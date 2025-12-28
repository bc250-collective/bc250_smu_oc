# Credit to: https://github.com/irusanov/ZenStates-Linux for implementation of smu access in python

import os
import struct

def _writesmureg(reg, value=0):
    if reg == -1:
        raise ValueError(f"smu register address was not properly initialized: {reg}")

    os.popen('setpci -v -s 0:0.0 b8.l={:08X}'.format(reg)).read()
    os.popen('setpci -v -s 0:0.0 bc.l={:08X}'.format(value)).read()


def _readsmureg(reg):
    if reg == -1:
        raise ValueError(f"smu register address was not properly initialized: {reg}")

    os.popen('setpci -v -s 0:0.0 b8.l={:08X}'.format(reg)).read()
    output = os.popen('setpci -v -s 0:0.0 bc.l').read()
    return int(output[-9:][0:8], 16)


class _bc250_smu_base:
    SMU_CMD_ADDR = -1
    SMU_RSP_ADDR = -1
    SMU_ARG_ADDR = -1

    MSG_TestMessage = 1
    MSG_GetSmuVersion = 2

    def _writesmu(self, cmd, value=0):
        res = False
        # clear the response register
        _writesmureg(self.SMU_RSP_ADDR, 0)
        # write the value
        _writesmureg(self.SMU_ARG_ADDR, value)
        _writesmureg(self.SMU_ARG_ADDR + 4, 0)
        # send the command
        _writesmureg(self.SMU_CMD_ADDR, cmd)
        #wait for completion
        self._smuwaitdone()
        #return status
        return _readsmureg(self.SMU_RSP_ADDR)

    def _smuwaitdone(self):
        res = False
        timeout = 100
        data = 0
        while ((not res or data != 1) and timeout > 0):
            timeout-=1
            data = _readsmureg(self.SMU_RSP_ADDR)
            if data == 1:
                res = True
            if (timeout == 0 or data != 1):
                res = False
        return res

    def write(self, cmd, value = 0):
        status = self._writesmu(cmd, value)
        if status != 1:
            raise ValueError(f"smu returned unexpected status {status}")

    def read(self):
        return _readsmureg(self.SMU_ARG_ADDR)

    def read_high(self):
        return _readsmureg(self.SMU_ARG_ADDR + 4)

    # The only 2 common messages
    def check_test_message(self):
        value = 123
        self.write(self.MSG_TestMessage, value)

        response = self.read()
        if response != value + 1:
            raise ValueError(f"smu returned unexpected test value {response}, expected {value+1}")

        return True

    def get_smu_version(self):
        self.write(self.MSG_GetSmuVersion)
        return self.read()

# Remote SMU
class bc250_rsmu(_bc250_smu_base):
    SMU_CMD_ADDR = 0x03B10A20
    SMU_RSP_ADDR = 0x03B10A80
    SMU_ARG_ADDR = 0x03B10A88

    MSG_set_boost_clock = 0x8F
    MSG_set_core_clock_stretch = 0x52
    MSG_set_ccx_clock_stretch = 0x53
    MSG_set_vid_scaling = 0x50
    MSG_set_vid_offset = 0x4D
    MSG_set_extra_voltage = 0x9A
    MSG_set_cpu_max_temp = 0x8B
    MSG_set_gpu_max_temp = 0x8C
    MSG_get_cpu_vid = 0x36
    MSG_get_core_clock = 0x43

    def set_boost_clock(self, clock):
        """boost clock in MHz"""
        self.write(self.MSG_set_boost_clock, clock)

    def set_core_clock_stretch(self, factor):
        """factor 0 - 1000 (gets scaled to 0 - 1)"""
        self.write(self.MSG_set_core_clock_stretch, factor)

    def set_ccx_clock_stretch(self, factor):
        """factor 0 - 1000 (gets scaled to 0 - 1)"""
        self.write(self.MSG_set_ccx_clock_stretch, factor)

    def set_vid_scaling(self, scaling):
        """scaling factor is integer (0 is default)"""
        self.write(self.MSG_set_vid_scaling, struct.unpack('<I', struct.pack('<h', scaling) + b'\x00\x00')[0])

    def set_vid_offset(self, offset):
        """offset in Volt"""
        self.write(self.MSG_set_vid_offset, struct.unpack('<I', struct.pack('<f', offset))[0])

    def disable_extra_voltage(self, flag):
        """True disables extra voltage"""
        if flag:
            self.write(self.MSG_set_extra_voltage, 1)
        else:
            self.write(self.MSG_set_extra_voltage, 0)

    def set_cpu_max_temp(self, temp):
        """Temp in deg C"""
        self.write(self.MSG_set_cpu_max_temp, temp)

    def set_gpu_max_temp(self, temp):
        """Temp in deg C"""
        self.write(self.MSG_set_gpu_max_temp, temp)

    def get_cpu_vid(self):
        """returns vid in mV"""
        self.write(self.MSG_get_cpu_vid)
        return self.read()

    def get_core_clock(self, core):
        """core 0 - 7"""
        self.write(self.MSG_get_core_clock, core)
        return self.read()



# Graphics SMU
# Warning: Access can collide with amdgpu driver!
class bc250_gsmu(_bc250_smu_base):
    SMU_CMD_ADDR = 0x03B10A08
    SMU_RSP_ADDR = 0x03B10A68
    SMU_ARG_ADDR = 0x03B10A48
