from .codec import decode_u32, pack_s16, pack_u32, pack_vid_offset


class Queue3Mixin:
    def _set_boost_clock(self, clock_mhz: int) -> None:
        self.send_message(3, 0x8F, arg=clock_mhz, pack=pack_u32)

    def _set_core_clock_stretch(self, factor: int) -> None:
        self.send_message(3, 0x52, arg=factor, pack=pack_u32)

    def _set_ccx_clock_stretch(self, factor: int) -> None:
        self.send_message(3, 0x53, arg=factor, pack=pack_u32)

    def _set_vid_scaling(self, scaling: int) -> None:
        self.send_message(3, 0x50, arg=scaling, pack=pack_s16)

    def _set_vid_offset(self, volts: float) -> None:
        self.send_message(3, 0x49, arg=volts, pack=pack_vid_offset)

    def _disable_extra_voltage(self, flag: bool) -> None:
        self.send_message(3, 0x9A, arg=1 if flag else 0, pack=pack_u32)

    def _set_cpu_max_temp(self, temp_c: int) -> None:
        self.send_message(3, 0x8B, arg=temp_c, pack=pack_u32)

    def _set_gpu_max_temp(self, temp_c: int) -> None:
        self.send_message(3, 0x8C, arg=temp_c, pack=pack_u32)

    def _get_cpu_vid(self) -> int:
        return self.send_message(3, 0x36, decode=decode_u32)

    def _get_core_clock(self, core_id: int) -> int:
        return self.send_message(3, 0x43, arg=core_id, pack=pack_u32, decode=decode_u32)

    def _q3_0x04(self) -> int | None:
        return self.send_message(3, 0x04)

    def _q3_0x0a(self) -> int | None:
        return self.send_message(3, 0x0A)

    def _q3_0x0b(self) -> int | None:
        return self.send_message(3, 0x0B)

    def _q3_0x0c(self) -> int | None:
        return self.send_message(3, 0x0C)

    def _q3_0x0d(self) -> int | None:
        return self.send_message(3, 0x0D)

    def _q3_0x0e(self) -> int | None:
        return self.send_message(3, 0x0E)

    def _q3_0x0f_set_cpu_gpu_vid(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x0F, arg=value, pack=pack_u32)

    def _q3_0x10_unforce_cpu_gpu_vid(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x10, arg=value, pack=pack_u32)

    def _q3_0x11(self) -> int | None:
        return self.send_message(3, 0x11)

    def _q3_0x14(self) -> int | None:
        return self.send_message(3, 0x14)

    def _q3_0x15(self) -> int | None:
        return self.send_message(3, 0x15)

    def _q3_0x18(self) -> int | None:
        return self.send_message(3, 0x18)

    def _q3_0x19(self) -> int | None:
        return self.send_message(3, 0x19)

    def _q3_0x1a(self) -> int | None:
        return self.send_message(3, 0x1A)

    def _q3_0x1b(self) -> int | None:
        return self.send_message(3, 0x1B)

    def _q3_0x1d_set_soc_clock_for_index(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x1D, arg=value, pack=pack_u32)

    def _q3_0x1e_set_perfprofileindex(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x1E, arg=value, pack=pack_u32)

    def _q3_0x20_set_max_temperature_cpu_gpu(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x20, arg=value, pack=pack_u32)

    def _q3_0x24(self) -> int | None:
        return self.send_message(3, 0x24)

    def _q3_0x25_set_oc_clk(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x25, arg=value, pack=pack_u32)

    def _q3_0x26_unset_oc_clk(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x26, arg=value, pack=pack_u32)

    def _q3_0x27_secure_access(self) -> int | None:
        return self.send_message(3, 0x27)

    def _q3_0x28_write_to_dat_8b08_secure(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x28, arg=value, pack=pack_u32)

    def _q3_0x29_write_to_pointer_at_dat(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x29, arg=value, pack=pack_u32)

    def _q3_0x2a_secure_access(self) -> int | None:
        return self.send_message(3, 0x2A)

    def _q3_0x2b_writes_into_dat_00008b0c(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x2B, arg=value, pack=pack_u32)

    def _q3_0x2c_secure_access(self) -> int | None:
        return self.send_message(3, 0x2C)

    def _q3_0x2d_secure_access(self) -> int | None:
        return self.send_message(3, 0x2D)

    def _q3_0x2e_secure_access(self) -> int | None:
        return self.send_message(3, 0x2E)

    def _q3_0x2f_secure_access(self) -> int | None:
        return self.send_message(3, 0x2F)

    def _q3_0x30_return_cpu_vid_float_or(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x30, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x34_return_dat_00015778(self) -> int | None:
        return self.send_message(3, 0x34, decode=decode_u32)

    def _q3_0x36_get_current_cpu_voltage(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x36, decode=decode_u32)

    def _q3_0x37_get_current_gpu_voltage(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x37, decode=decode_u32)

    def _q3_0x38_get_more_clock_assigned_to_state(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x38, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x39_get_other_clock_assigned_to_s(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x39, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x3a_get_some_clock_assigned_to_state(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x3A, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x3b_get_clk_assigned_to_p_state(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x3B, arg=value, pack=pack_u32, decode=decode_u32)

    def _q2_0x05_enable_smu_features_3c(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x3C, arg=value, pack=pack_u32)

    def _q2_0x06_disable_smu_features_3d(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x3D, arg=value, pack=pack_u32)

    def _q3_0x40_get_cpu_temp_max(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x40, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x41_read_from_perfprofiletable(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x41, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x42_return_vddcrsoc_dpm_value(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x42, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x43_get_core_freq(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x43, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x47_return_status_0xfe(self) -> int | None:
        return self.send_message(3, 0x47, decode=decode_u32)

    def _q3_0x48_return_status_0xfe(self) -> int | None:
        return self.send_message(3, 0x48, decode=decode_u32)

    def _q3_0x49_set_cpu_vid_offset(self, volts: float = 0.0) -> int | None:
        return self.send_message(3, 0x49, arg=volts, pack=pack_vid_offset)

    def _q3_0x4a_getgfxvidoffset1(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x4A, arg=value, pack=pack_u32)

    def _q2_0x17_cpu_droop_calibration_4b(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x4B, arg=value, pack=pack_u32)

    def _q3_0x4c_gfx_droop_calibration(self) -> int | None:
        return self.send_message(3, 0x4C)

    def _q3_0x4d_set_cpu_vid_offset_large(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x4D, arg=value, pack=pack_u32)

    def _q3_0x4e_set_gpu_vid_offset_largee(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x4E, arg=value, pack=pack_u32)

    def _q3_0x4f(self) -> int | None:
        return self.send_message(3, 0x4F)

    def _q3_0x50_scale_f_vid_curve(self, scaling: int = 0) -> int | None:
        return self.send_message(3, 0x50, arg=scaling, pack=pack_s16)

    def _q3_0x51_set_cpu_coeff(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x51, arg=value, pack=pack_u32)

    def _q3_0x52_set_cpu_clock_stretch_coeff(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x52, arg=value, pack=pack_u32)

    def _q3_0x53_set_ccx_clock_stretch_coeff(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x53, arg=value, pack=pack_u32)

    def _q3_0x54(self) -> int | None:
        return self.send_message(3, 0x54)

    def _q3_0x55(self) -> int | None:
        return self.send_message(3, 0x55)

    def _q3_0x56(self) -> int | None:
        return self.send_message(3, 0x56)

    def _q3_0x58(self) -> int | None:
        return self.send_message(3, 0x58)

    def _q3_0x59(self) -> int | None:
        return self.send_message(3, 0x59)

    def _q3_0x5a(self) -> int | None:
        return self.send_message(3, 0x5A)

    def _q3_0x5b(self) -> int | None:
        return self.send_message(3, 0x5B)

    def _q3_0x5c_something_freq_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x5C, arg=value, pack=pack_u32)

    def _q3_0x5d_something_freq_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x5D, arg=value, pack=pack_u32)

    def _q3_0x5e(self) -> int | None:
        return self.send_message(3, 0x5E)

    def _q3_0x5f_write_somecpu_frequency(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x5F, arg=value, pack=pack_u32)

    def _q3_0x60_somthing_pstate_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x60, arg=value, pack=pack_u32)

    def _q3_0x65_set_dat_000133fc_value(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x65, arg=value, pack=pack_u32)

    def _q3_0x66_reset_dat_000133fc_value_to_0(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x66, arg=value, pack=pack_u32)

    def _q3_0x67_zero_return(self) -> int | None:
        return self.send_message(3, 0x67)

    def _q3_0x6a(self) -> int | None:
        return self.send_message(3, 0x6A)

    def _q3_0x6b(self) -> int | None:
        return self.send_message(3, 0x6B)

    def _q3_0x6c_set_temperature_parameters(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x6C, arg=value, pack=pack_u32)

    def _q3_0x6d_force_clock_stretching_vid(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x6D, arg=value, pack=pack_u32)

    def _q3_0x6e_cpu_coefficients(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x6E, arg=value, pack=pack_u32)

    def _q3_0x6f(self) -> int | None:
        return self.send_message(3, 0x6F)

    def _q3_0x70(self) -> int | None:
        return self.send_message(3, 0x70)

    def _q3_0x71(self) -> int | None:
        return self.send_message(3, 0x71)

    def _q3_0x72(self) -> int | None:
        return self.send_message(3, 0x72)

    def _q3_0x73(self) -> int | None:
        return self.send_message(3, 0x73)

    def _q3_0x74(self) -> int | None:
        return self.send_message(3, 0x74)

    def _q3_0x75(self) -> int | None:
        return self.send_message(3, 0x75)

    def _q3_0x76(self) -> int | None:
        return self.send_message(3, 0x76)

    def _q3_0x77_set_cpu_max_current_or_power(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x77, arg=value, pack=pack_u32, decode=decode_u32)

    def _q3_0x7f_get_current_perf_sample(self) -> int | None:
        return self.send_message(3, 0x7F, decode=decode_u32)

    def _q3_0x80_get_sample_interval_max(self) -> int | None:
        return self.send_message(3, 0x80, decode=decode_u32)

    def _q3_0x85(self) -> int | None:
        return self.send_message(3, 0x85)

    def _q3_0x86(self) -> int | None:
        return self.send_message(3, 0x86)

    def _q3_0x87(self) -> int | None:
        return self.send_message(3, 0x87)

    def _q3_0x8b_set_cpu_max_temperature(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x8B, arg=value, pack=pack_u32)

    def _q3_0x8c_set_gpu_max_temperature(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x8C, arg=value, pack=pack_u32)

    def _q3_0x8d_get_current_sample_interval(self) -> int | None:
        return self.send_message(3, 0x8D, decode=decode_u32)

    def _q3_0x8e_set_vid_main_2_limit(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x8E, arg=value, pack=pack_u32)

    def _q3_0x8f_set_max_cpu_boost_clk(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x8F, arg=value, pack=pack_u32)

    def _q3_0x90(self) -> int | None:
        return self.send_message(3, 0x90)

    def _q3_0x91(self) -> int | None:
        return self.send_message(3, 0x91)

    def _q3_0x96(self) -> int | None:
        return self.send_message(3, 0x96)

    def _q3_0x98(self) -> int | None:
        return self.send_message(3, 0x98)

    def _q3_0x99_modify_p_state_0_parameter_an(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x99, arg=value, pack=pack_u32)

    def _q3_0x9a_set_vid_extra_voltage_flags(self, value: int = 0) -> int | None:
        return self.send_message(3, 0x9A, arg=value, pack=pack_u32)

    def _q3_0x9b_switch_core_bilinear_model(self) -> int | None:
        return self.send_message(3, 0x9B)

    def _q3_0x9c(self) -> int | None:
        return self.send_message(3, 0x9C)

    def _q3_0xa7_cpu_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0xA7, arg=value, pack=pack_u32)

    def _q3_0xa8_cpu_related(self, value: int = 0) -> int | None:
        return self.send_message(3, 0xA8, arg=value, pack=pack_u32)
