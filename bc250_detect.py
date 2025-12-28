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

def vid_predict_delta(clock_cur, clock_next, scale):
    if clock_cur < 3000 or clock_next < 3000:
        return 0
    return vid_predict(clock_next, scale) - vid_predict(clock_cur, scale)

def vid_predict_relative(clock_cur, clock_next, scale, vid_cur):
    return vid_cur + vid_predict_delta(clock_cur, clock_next, scale)

def smu_apply(clock, scale):
    global smu
    res = input(f"Apply {clock} MHz @ {scale} ? ")
    if res == 'y':
        smu.set_vid_scaling(scale)
        smu.set_boost_clock(clock)
        print("Applied")
    else:
        print("Aborted")

# This is not finished
def detect(f_target, v_max, t_max):
    global smu
    f_step = 50
    delay_short = 1
    delay_long = 10

    f_test = 3500
    f_safe = 3500
    v_scale_test = 0
    v_scale_safe = 0

    # set safe temperature limits
    smu.set_cpu_max_temp(t_max)
    smu.set_gpu_max_temp(t_max)
    # always disable extra voltage
    smu.disable_extra_voltage(True)

    smu_apply(3500, 0)



smu = bc250_rsmu()
smu.check_test_message()
print("Test Message OK")
detect(3700, 1300, 90)
print("Done")
