#!/usr/bin/env python
import struct
import time
import pandas as pd

from bc250_smu import bc250_rsmu
from stress_helper import *

def vid_predict(clock, scale):
    if clock < 3000:
        raise ValueError("cannot predict vid for clocks below 3 GHz")
    p = -1.519 + scale * 0.004325
    q = 2800.0 - (scale * 10.0)
    return 0.0003 * clock * clock + p * clock + q

def vid_predict_delta(clock_cur, clock_next, scale_cur, scale_next):
    if clock_cur < 3000 or clock_next < 3000:
        return 0
    return vid_predict(clock_next, scale_next) - vid_predict(clock_cur, scale_cur)

def vid_predict_relative(clock_cur, clock_next, scale_cur, scale_next, vid_cur):
    # We scale our predction by 0.8 to bias it towards the upper limit
    return vid_cur + (vid_predict_delta(clock_cur, clock_next, scale_cur, scale_next) * 0.8)

def smu_apply(clock, scale):
    global smu
    res = input(f"Apply {clock} MHz @ scale {scale} (y/n)? ")
    if res == 'y':
        smu.set_vid_scaling(scale)
        smu.set_boost_clock(clock)
        print("Applied")
    else:
        print("Aborted")

# This is not finished
def detect(f_target, v_max, t_max):
    global smu

    f_step = 100
    delay_short = 1
    delay_long = 5

    f_test = 3500
    f_safe = 3500
    v_scale_test = 0
    v_scale_safe = 0

    # set safe temperature limits
    smu.set_cpu_max_temp(t_max)
    smu.set_gpu_max_temp(t_max)
    # always disable extra voltage
    smu.disable_extra_voltage(True)

    while f_safe < f_target:
        print(f"========== OC Step {f_test} MHz =========")
        smu_apply(f_test, v_scale_test)

        stress_start()
        time.sleep(delay_short)

        v_meas = smu.get_cpu_vid()
        print(f"Measured vid for this iteration: {v_meas} mV")
        if v_meas > v_max:
            stress_stop()
            print(f"retry and reduce vid because it overshot by {v_meas - v_max} mV")
            v_scale_test -= int((v_meas - v_max) / 6.0) # estimate the required undervolt
            continue

        print("Stress Testing")
        time.sleep(delay_long)

        #Check Throttling here

        stress_stop()

        f_safe = f_test
        v_scale_safe = v_scale_test
        #write out config here

        f_test += f_step

        v_pred = vid_predict_relative(f_safe, f_test, v_scale_safe, v_scale_test, v_meas)
        while(v_pred > v_max):
            v_scale_test -= 1
            v_pred = vid_predict_relative(f_safe, f_test, v_scale_safe, v_scale_test, v_meas)

        print(f"Adjusted vid prediction for next iteration: {v_pred} mV @ scale {v_scale_test}")

    print(f"\n\n\nFinal Result: {f_safe} MHz @ {v_meas} mV using scale {v_scale_safe}")
    print("Answer y to reset to default values, n to keep the overclock")
    smu_apply(3500, 0)


smu = bc250_rsmu()
smu.check_test_message()
print("Test Message OK")
detect(3900, 1250, 90)
print("Done")
