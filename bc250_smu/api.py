import struct
from typing import Callable, Dict, Optional, Tuple

from .mailbox import Bc250Mailbox
from .transport import Bc250PciTransport


DEFAULT_QUEUE_ADDRS: Dict[int, Tuple[int, int, int]] = {
    0: (0x03B10A08, 0x03B10A68, 0x03B10A48),
    3: (0x03B10A20, 0x03B10A80, 0x03B10A88),
}


def pack_u32(value: int) -> int:
    return int(value) & 0xFFFFFFFF


def pack_s16(value: int) -> int:
    return struct.unpack("<I", struct.pack("<h", int(value)) + b"\x00\x00")[0]


def pack_f32(value: float) -> int:
    return struct.unpack("<I", struct.pack("<f", float(value)))[0]


def pack_vid_offset(volts: float) -> int:
    return pack_f32(volts)


def decode_u32(value: int) -> int:
    return int(value) & 0xFFFFFFFF


class Bc250Smu:
    def __init__(
        self,
        bdf: str = "0000:00:00.0",
        allow_queue1: bool = False,
        use_flock: bool = False,
        queue_addrs: Optional[Dict[int, Tuple[int, int, int]]] = None,
        timeout: int = 100,
    ) -> None:
        self._allow_queue1 = allow_queue1
        self._transport = Bc250PciTransport(bdf=bdf, use_flock=use_flock)
        self._transport.open()
        addrs = dict(DEFAULT_QUEUE_ADDRS)
        if queue_addrs:
            addrs.update(queue_addrs)
        self._queues: Dict[int, Bc250Mailbox] = {
            queue: Bc250Mailbox(self._transport, cmd, rsp, arg, timeout=timeout)
            for queue, (cmd, rsp, arg) in addrs.items()
        }

    def close(self) -> None:
        self._transport.close()

    def raw_send(self, queue: int, msg_id: int, arg: int = 0, arg_high: Optional[int] = None) -> int:
        self._guard_queue(queue)
        return self._get_queue(queue).send(msg_id, arg=arg, arg_high=arg_high)

    def raw_read(self, queue: int) -> int:
        self._guard_queue(queue)
        return self._get_queue(queue).read_arg()

    def raw_read_high(self, queue: int) -> int:
        self._guard_queue(queue)
        return self._get_queue(queue).read_arg_high()

    def send_message(
        self,
        queue_id: int,
        msg_id: int,
        arg: int = 0,
        arg_high: Optional[int] = None,
        pack: Optional[Callable[[int], int]] = None,
        decode: Optional[Callable[[int], int]] = None,
        check_status: bool = True,
    ) -> int:
        packed = pack(arg) if pack is not None else pack_u32(arg)
        status = self.raw_send(queue_id, msg_id, arg=packed, arg_high=arg_high)
        if check_status and status != Bc250Mailbox.SMU_RETURN_OK:
            raise RuntimeError(f"smu returned status 0x{status:02X} for queue {queue_id} msg 0x{msg_id:02X}")
        if decode is None:
            return status
        return decode(self.raw_read(queue_id))

    def test_message(self, value: int) -> bool:
        response = self.send_message(
            0,
            0x01,
            arg=value,
            pack=pack_u32,
            decode=decode_u32,
        )
        if response != value + 1:
            raise RuntimeError(f"unexpected test response {response}, expected {value + 1}")
        return True


    # TESTED MESSAGES:





    # UNTESTED MESSAGES:
    # QUEUE 0
    def get_smu_version(self) -> int:
        return self.send_message(0, 0x02, decode=decode_u32)

    def get_driver_if_version(self) -> int:
        return self.send_message(0, 0x03, decode=decode_u32)

    def set_driver_table_dram_addr_high(self, value: int) -> None:
        self.send_message(0, 0x04, arg=value, pack=pack_u32)

    def set_driver_table_dram_addr_low(self, value: int) -> None:
        self.send_message(0, 0x05, arg=value, pack=pack_u32)

    def transfer_table_smu2dram(self) -> None:
        self.send_message(0, 0x06)

    def transfer_table_dram2smu(self) -> None:
        self.send_message(0, 0x07)

    def request_core_pstate(self, core_id: int) -> None:
        self.send_message(0, 0x0B, arg=core_id, pack=pack_u32)

    def query_core_pstate(self, core_id: int) -> int:
        return self.send_message(
            0,
            0x0C,
            arg=core_id,
            pack=pack_u32,
            decode=decode_u32,
            check_status=False,
        )

    def request_gfxclk(self) -> None:
        self.send_message(0, 0x0E)

    def query_gfxclk(self) -> int:
        return self.send_message(0, 0x0F, decode=decode_u32)

    def query_vddcr_soc_clock(self) -> int:
        return self.send_message(0, 0x11, decode=decode_u32)

    def query_df_pstate(self) -> int:
        return self.send_message(0, 0x13, decode=decode_u32)

    def configure_s3_pwroff_register_addr_high(self, value: int) -> None:
        self.send_message(0, 0x16, arg=value, pack=pack_u32)

    def configure_s3_pwroff_register_addr_low(self, value: int) -> None:
        self.send_message(0, 0x17, arg=value, pack=pack_u32)

    def request_active_wgp(self) -> None:
        self.send_message(0, 0x18)

    def set_min_deep_sleep_gfxclk_freq(self, value: int) -> None:
        self.send_message(0, 0x19, arg=value, pack=pack_u32)

    def set_max_deep_sleep_dfll_gfx_div(self, value: int) -> None:
        self.send_message(0, 0x1A, arg=value, pack=pack_u32)

    def start_telemetry_reporting(self, value: int = 0) -> None:
        self.send_message(0, 0x1B, arg=value, pack=pack_u32)

    def stop_telemetry_reporting(self) -> None:
        self.send_message(0, 0x1C)

    def clear_telemetry_max(self) -> None:
        self.send_message(0, 0x1D)

    def query_active_wgp(self) -> int:
        return self.send_message(0, 0x1E, decode=decode_u32)

    def get_gfx_frequency(self) -> int:
        return self.send_message(0, 0x37, decode=decode_u32)

    def get_gfx_vid(self) -> int:
        return self.send_message(0, 0x38, decode=decode_u32)

    def force_gfx_freq(self, mhz_freq: int) -> None:
        self.send_message(0, 0x39, arg=mhz_freq, pack=pack_u32)

    def unforce_gfx_freq(self) -> None:
        self.send_message(0, 0x3A)

    def force_gfx_vid(self, vid: int) -> None:
        self.send_message(0, 0x3B, arg=vid, pack=pack_u32)

    def unforce_gfx_vid(self) -> None:
        self.send_message(0, 0x3C)

    def get_enabled_smu_features(self) -> int:
        return self.send_message(0, 0x3D, decode=decode_u32)

    def set_core_enable_mask(self, mask: int) -> None:
        self.send_message(0, 0x2C, arg=mask, pack=pack_u32)

    def gfx_cac_weight_operation(self, value: int) -> None:
        self.send_message(0, 0x2F, arg=value, pack=pack_u32)

    def l3_cac_weight_operation(self, value: int) -> None:
        self.send_message(0, 0x30, arg=value, pack=pack_u32)

    def pack_core_cac_weight(self, value: int) -> None:
        self.send_message(0, 0x31, arg=value, pack=pack_u32)

    def set_driver_table_vmid(self, value: int) -> None:
        self.send_message(0, 0x34, arg=value, pack=pack_u32)

    def set_soft_min_cclk(self, value: int) -> None:
        self.send_message(0, 0x35, arg=value, pack=pack_u32)

    def set_soft_max_cclk(self, value: int) -> None:
        self.send_message(0, 0x36, arg=value, pack=pack_u32)

    # QUEUE 1
    def q1_0x08(self) -> int | None:
        return self.send_message(1, 0x08)

    def q1_0x10(self) -> int | None:
        return self.send_message(1, 0x10)

    # QUEUE 2
    def q2_0x04_get_device_name(self) -> int | None:
        return self.send_message(2, 0x04, decode=decode_u32)

    def q2_0x05_enable_smu_features(self, value: int = 0) -> int | None:
        return self.send_message(2, 0x05, arg=value, pack=pack_u32)

    def q2_0x06_disable_smu_features(self, value: int = 0) -> int | None:
        return self.send_message(2, 0x06, arg=value, pack=pack_u32)

    def q2_0x07(self) -> int | None:
        return self.send_message(2, 0x07)

    def q2_0x08(self) -> int | None:
        return self.send_message(2, 0x08)

    def q2_0x09(self) -> int | None:
        return self.send_message(2, 0x09)

    def q2_0x0a(self) -> int | None:
        return self.send_message(2, 0x0A)

    def q2_0x0b(self) -> int | None:
        return self.send_message(2, 0x0B)

    def q2_0x0c(self) -> int | None:
        return self.send_message(2, 0x0C)

    def q2_message_set_some_other_addr_high(self, value: int = 0) -> int | None:
        return self.send_message(2, 0x0D, arg=value, pack=pack_u32)

    def q2_message_set_some_other_addr_low(self, value: int = 0) -> int | None:
        return self.send_message(2, 0x0E, arg=value, pack=pack_u32)

    def q2_0x3e(self) -> int | None:
        return self.send_message(2, 0x0F)

    def q2_0x3f(self) -> int | None:
        return self.send_message(2, 0x10)

    def q2_0x13(self) -> int | None:
        return self.send_message(2, 0x13)

    def q2_0x14(self) -> int | None:
        return self.send_message(2, 0x14)

    def q2_0x15(self) -> int | None:
        return self.send_message(2, 0x15)

    def q2_0x16(self) -> int | None:
        return self.send_message(2, 0x16)

    def q2_0x17_cpu_droop_calibration(self, value: int = 0) -> int | None:
        return self.send_message(2, 0x17, arg=value, pack=pack_u32)

    def q2_0x1a(self) -> int | None:
        return self.send_message(2, 0x1A)

    def q2_0x20(self) -> int | None:
        return self.send_message(2, 0x20)

    def q2_0x21(self) -> int | None:
        return self.send_message(2, 0x21)

    def q2_0x22(self) -> int | None:
        return self.send_message(2, 0x22)

    def q2_0x23(self) -> int | None:
        return self.send_message(2, 0x23)

    def q2_0x29(self) -> int | None:
        return self.send_message(2, 0x29)

    def q2_0x2c_probably_power_limit_settings(self) -> int | None:
        return self.send_message(2, 0x2C)

    def q2_0x2d_sibling_of_0x2c_but_returns_v(self) -> int | None:
        return self.send_message(2, 0x2D)

    def q2_0x2e(self) -> int | None:
        return self.send_message(2, 0x2E)

    def q2_0x2f(self) -> int | None:
        return self.send_message(2, 0x2F)

    def q2_0x30(self) -> int | None:
        return self.send_message(2, 0x30)


    # QUEUE 3
    def q3_0x04(self) -> int | None:
        return self.send_message(3, 0x04)

    def q3_0x0a(self) -> int | None:
        return self.send_message(3, 0x0A)

    def q3_0x0b(self) -> int | None:
        return self.send_message(3, 0x0B)

    def q3_0x0c(self) -> int | None:
        return self.send_message(3, 0x0C)

    def q3_0x0d(self) -> int | None:
        return self.send_message(3, 0x0D)

    def q3_0x0e(self) -> int | None:
        return self.send_message(3, 0x0E)

    def q3_0x0f_set_cpu_gpu_vid(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x0F, arg=value, pack=pack_u32)

    def q3_0x10_unforce_cpu_gpu_vid(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x10, arg=value, pack=pack_u32)

    def q3_0x11(self) -> int | None:
        return self.send_message(3, 0x11)

    def q3_0x14(self) -> int | None:
        return self.send_message(3, 0x14)

    def q3_0x15(self) -> int | None:
        return self.send_message(3, 0x15)

    def q3_0x18(self) -> int | None:
        return self.send_message(3, 0x18)

    def q3_0x19(self) -> int | None:
        return self.send_message(3, 0x19)

    def q3_0x1a(self) -> int | None:
        return self.send_message(3, 0x1A)

    def q3_0x1b(self) -> int | None:
        return self.send_message(3, 0x1B)

    def q3_0x1d_set_soc_clock_for_index(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x1D, arg=value, pack=pack_u32)

    def q3_0x1e_set_perfprofileindex(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x1E, arg=value, pack=pack_u32)

    def q3_0x20_set_max_temperature_cpu_gpu(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x20, arg=value, pack=pack_u32)

    def q3_0x24(self) -> int | None:
        return self.send_message(3, 0x24)

    def q3_0x25_set_oc_clk(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x25, arg=value, pack=pack_u32)

    def q3_0x26_unset_oc_clk(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x26, arg=value, pack=pack_u32)

    def q3_0x27_secure_access(self) -> int | None:
        return self.send_message(3, 0x27)

    def q3_0x28_write_to_dat_8b08_secure(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x28, arg=value, pack=pack_u32)

    def q3_0x29_write_to_pointer_at_dat(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x29, arg=value, pack=pack_u32)

    def q3_0x2a_secure_access(self) -> int | None:
        return self.send_message(3, 0x2A)

    def q3_0x2b_writes_into_dat_00008b0c(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x2B, arg=value, pack=pack_u32)

    def q3_0x2c_secure_access(self) -> int | None:
        return self.send_message(3, 0x2C)

    def q3_0x2d_secure_access(self) -> int | None:
        return self.send_message(3, 0x2D)

    def q3_0x2e_secure_access(self) -> int | None:
        return self.send_message(3, 0x2E)

    def q3_0x2f_secure_access(self) -> int | None:
        return self.send_message(3, 0x2F)

    def q3_0x30_return_cpu_vid_float_or(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x30, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x34_return_dat_00015778(self) -> int | None:
        return self.send_message(3, 0x34, decode=decode_u32)

    def q3_0x36_get_current_cpu_voltage(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x36, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x37_get_current_gpu_voltage(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x37, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x38_get_more_clock_assigned_to_state(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x38, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x39_get_other_clock_assigned_to_s(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x39, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x3a_get_some_clock_assigned_to_state(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x3A, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x3b_get_clk_assigned_to_p_state(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x3B, arg=value, pack=pack_u32, decode=decode_u32)

    def q2_0x05_enable_smu_features_3c(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x3C, arg=value, pack=pack_u32)

    def q2_0x06_disable_smu_features_3d(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x3D, arg=value, pack=pack_u32)

    def q3_0x40_get_cpu_temp_max(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x40, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x41_read_from_perfprofiletable(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x41, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x42_return_vddcrsoc_dpm_value(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x42, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x43_get_core_freq(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x43, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x47_return_status_0xfe(self) -> int | None:
        return self.send_message(3, 0x47, decode=decode_u32)

    def q3_0x48_return_status_0xfe(self) -> int | None:
        return self.send_message(3, 0x48, decode=decode_u32)

    def q3_0x49_set_cpu_vid_offset(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x49, arg=value, pack=pack_u32)

    def q3_0x4a_getgfxvidoffset1(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x4A, arg=value, pack=pack_u32)

    def q2_0x17_cpu_droop_calibration_4b(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x4B, arg=value, pack=pack_u32)

    def q3_0x4c_gfx_droop_calibration(self) -> int | None:
        return self.send_message(3, 0x4C)

    def q3_0x4d_set_cpu_vid_offset_large(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x4D, arg=value, pack=pack_vid_offset)

    def q3_0x4e_set_gpu_vid_offset_large(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x4E, arg=value, pack=pack_vid_offset)

    def q3_0x4f(self) -> int | None:
        return self.send_message(3, 0x4F)

    def q3_0x50_scale_f_vid_curve(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x50, arg=value, pack=pack_s16)

    def q3_0x51_set_cpu_coeff(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x51, arg=value, pack=pack_u32)

    def q3_0x52_set_cpu_clock_stretch_coeff(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x52, arg=value, pack=pack_u32)

    def q3_0x53_set_ccx_clock_stretch_coeff(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x53, arg=value, pack=pack_u32)

    def q3_0x54(self) -> int | None:
        return self.send_message(3, 0x54)

    def q3_0x55(self) -> int | None:
        return self.send_message(3, 0x55)

    def q3_0x56(self) -> int | None:
        return self.send_message(3, 0x56)

    def q3_0x58(self) -> int | None:
        return self.send_message(3, 0x58)

    def q3_0x59(self) -> int | None:
        return self.send_message(3, 0x59)

    def q3_0x5a(self) -> int | None:
        return self.send_message(3, 0x5A)

    def q3_0x5b(self) -> int | None:
        return self.send_message(3, 0x5B)

    def q3_0x5c_something_freq_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x5C, arg=value, pack=pack_u32)

    def q3_0x5d_something_freq_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x5D, arg=value, pack=pack_u32)

    def q3_0x5e(self) -> int | None:
        return self.send_message(3, 0x5E)

    def q3_0x5f_write_somecpu_frequency(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x5F, arg=value, pack=pack_u32)

    def q3_0x60_somthing_pstate_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x60, arg=value, pack=pack_u32)

    def q3_0x65_set_dat_000133fc_value(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x65, arg=value, pack=pack_u32)

    def q3_0x66_reset_dat_000133fc_value_to_0(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x66, arg=value, pack=pack_u32)

    def q3_0x67_zero_return(self) -> int | None:
        return self.send_message(3, 0x67)

    def q3_0x6a(self) -> int | None:
        return self.send_message(3, 0x6A)

    def q3_0x6b(self) -> int | None:
        return self.send_message(3, 0x6B)

    def q3_0x6c_set_temperature_parameters(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x6C, arg=value, pack=pack_u32)

    def q3_0x6d_force_clock_stretching_vid(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x6D, arg=value, pack=pack_u32)

    def q3_0x6e_cpu_coefficients(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x6E, arg=value, pack=pack_u32)

    def q3_0x6f(self) -> int | None:
        return self.send_message(3, 0x6F)

    def q3_0x70(self) -> int | None:
        return self.send_message(3, 0x70)

    def q3_0x71(self) -> int | None:
        return self.send_message(3, 0x71)

    def q3_0x72(self) -> int | None:
        return self.send_message(3, 0x72)

    def q3_0x73(self) -> int | None:
        return self.send_message(3, 0x73)

    def q3_0x74(self) -> int | None:
        return self.send_message(3, 0x74)

    def q3_0x75(self) -> int | None:
        return self.send_message(3, 0x75)

    def q3_0x76(self) -> int | None:
        return self.send_message(3, 0x76)

    def q3_0x77_set_cpu_max_current_or_power(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x77, arg=value, pack=pack_u32, decode=decode_u32)

    def q3_0x7f_get_current_perf_sample(self) -> int | None:
        return self.send_message(3, 0x7F, decode=decode_u32)

    def q3_0x80_get_sample_interval_max(self) -> int | None:
        return self.send_message(3, 0x80, decode=decode_u32)

    def q3_0x85(self) -> int | None:
        return self.send_message(3, 0x85)

    def q3_0x86(self) -> int | None:
        return self.send_message(3, 0x86)

    def q3_0x87(self) -> int | None:
        return self.send_message(3, 0x87)

    def q3_0x8b_set_cpu_max_temperature(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x8B, arg=value, pack=pack_u32)

    def q3_0x8c_set_gpu_max_temperature(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x8C, arg=value, pack=pack_u32)

    def q3_0x8d_get_current_sample_interval(self) -> int | None:
        return self.send_message(3, 0x8D, decode=decode_u32)

    def q3_0x8e_set_vid_main_2_limit(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x8E, arg=value, pack=pack_u32)

    def q3_0x8f_set_max_cpu_boost_clk(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x8F, arg=value, pack=pack_u32)

    def q3_0x90(self) -> int | None:
        return self.send_message(3, 0x90)

    def q3_0x91(self) -> int | None:
        return self.send_message(3, 0x91)

    def q3_0x96(self) -> int | None:
        return self.send_message(3, 0x96)

    def q3_0x98(self) -> int | None:
        return self.send_message(3, 0x98)

    def q3_0x99_modify_p_state_0_parameter_an(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x99, arg=value, pack=pack_u32)

    def q3_0x9a_set_vid_extra_voltage_flags(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x9A, arg=value, pack=pack_u32)

    def q3_0x9b_switch_core_bilinear_model(self) -> int | None:
        return self.send_message(3, 0x9B)

    def q3_0x9c(self) -> int | None:
        return self.send_message(3, 0x9C)

    def q3_0xa7_cpu_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0xA7, arg=value, pack=pack_u32)

    def q3_0xa8_cpu_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0xA8, arg=value, pack=pack_u32)

    def q5_0x04(self) -> int | None:
        return self.send_message(4, 0x04)

    def q5_0x05(self) -> int | None:
        return self.send_message(4, 0x05)

    def q5_0x06(self) -> int | None:
        return self.send_message(4, 0x06)

    def q5_0x07(self) -> int | None:
        return self.send_message(4, 0x07)

    def q5_0x08(self) -> int | None:
        return self.send_message(4, 0x08)

    def q5_0x09(self) -> int | None:
        return self.send_message(4, 0x09)

    def q5_0x0a_freq_op1(self, value: int = 0) -> int | None:
        return self.send_message(4, 0x0A, arg=value, pack=pack_u32)

    def q5_0x0b(self) -> int | None:
        return self.send_message(4, 0x0B)

    def q5_0x0d(self) -> int | None:
        return self.send_message(4, 0x0D)

    def q5_0x10(self) -> int | None:
        return self.send_message(4, 0x10)

    def q5_0x11(self) -> int | None:
        return self.send_message(4, 0x11)

    def _get_queue(self, queue: int) -> Bc250Mailbox:
        if queue not in self._queues:
            raise KeyError(f"queue {queue} not configured")
        return self._queues[queue]

    def _guard_queue(self, queue: int) -> None:
        if queue == 1 and not self._allow_queue1:
            raise PermissionError("queue 1 access disabled; pass allow_queue1=True to enable")
