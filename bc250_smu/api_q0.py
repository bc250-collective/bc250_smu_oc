from .codec import decode_u32, pack_u32


class Queue0Mixin:
    def _get_smu_version(self) -> int:
        return self.send_message(0, 0x02, decode=decode_u32)

    def _get_driver_if_version(self) -> int:
        return self.send_message(0, 0x03, decode=decode_u32)

    def _set_driver_table_dram_addr_high(self, value: int) -> None:
        self.send_message(0, 0x04, arg=value, pack=pack_u32)

    def _set_driver_table_dram_addr_low(self, value: int) -> None:
        self.send_message(0, 0x05, arg=value, pack=pack_u32)

    def _transfer_table_smu2dram(self) -> None:
        self.send_message(0, 0x06)

    def _transfer_table_dram2smu(self) -> None:
        self.send_message(0, 0x07)

    def _request_core_pstate(self, core_id: int) -> None:
        self.send_message(0, 0x0B, arg=core_id, pack=pack_u32)

    def _query_core_pstate(self, core_id: int) -> int:
        return self.send_message(
            0,
            0x0C,
            arg=core_id,
            pack=pack_u32,
            decode=decode_u32,
            check_status=False,
        )

    def _request_gfxclk(self) -> None:
        self.send_message(0, 0x0E)

    def _query_gfxclk(self) -> int:
        return self.send_message(0, 0x0F, decode=decode_u32)

    def _query_vddcr_soc_clock(self) -> int:
        return self.send_message(0, 0x11, decode=decode_u32)

    def _query_df_pstate(self) -> int:
        return self.send_message(0, 0x13, decode=decode_u32)

    def _configure_s3_pwroff_register_addr_high(self, value: int) -> None:
        self.send_message(0, 0x16, arg=value, pack=pack_u32)

    def _configure_s3_pwroff_register_addr_low(self, value: int) -> None:
        self.send_message(0, 0x17, arg=value, pack=pack_u32)

    def _request_active_wgp(self) -> None:
        self.send_message(0, 0x18)

    def _set_min_deep_sleep_gfxclk_freq(self, value: int) -> None:
        self.send_message(0, 0x19, arg=value, pack=pack_u32)

    def _set_max_deep_sleep_dfll_gfx_div(self, value: int) -> None:
        self.send_message(0, 0x1A, arg=value, pack=pack_u32)

    def _start_telemetry_reporting(self, value: int = 0) -> None:
        self.send_message(0, 0x1B, arg=value, pack=pack_u32)

    def _stop_telemetry_reporting(self) -> None:
        self.send_message(0, 0x1C)

    def _clear_telemetry_max(self) -> None:
        self.send_message(0, 0x1D)

    def _query_active_wgp(self) -> int:
        return self.send_message(0, 0x1E, decode=decode_u32)

    def _get_gfx_frequency(self) -> int:
        return self.send_message(0, 0x37, decode=decode_u32)

    def _get_gfx_vid(self) -> int:
        return self.send_message(0, 0x38, decode=decode_u32)

    def _force_gfx_freq(self, mhz_freq: int) -> None:
        self.send_message(0, 0x39, arg=mhz_freq, pack=pack_u32)

    def _unforce_gfx_freq(self) -> None:
        self.send_message(0, 0x3A)

    def _force_gfx_vid(self, vid: int) -> None:
        self.send_message(0, 0x3B, arg=vid, pack=pack_u32)

    def _unforce_gfx_vid(self) -> None:
        self.send_message(0, 0x3C)

    def _get_enabled_smu_features(self) -> int:
        return self.send_message(0, 0x3D, decode=decode_u32)

    def _set_core_enable_mask(self, mask: int) -> None:
        self.send_message(0, 0x2C, arg=mask, pack=pack_u32)

    def _gfx_cac_weight_operation(self, value: int) -> None:
        self.send_message(0, 0x2F, arg=value, pack=pack_u32)

    def _l3_cac_weight_operation(self, value: int) -> None:
        self.send_message(0, 0x30, arg=value, pack=pack_u32)

    def _pack_core_cac_weight(self, value: int) -> None:
        self.send_message(0, 0x31, arg=value, pack=pack_u32)

    def _set_driver_table_vmid(self, value: int) -> None:
        self.send_message(0, 0x34, arg=value, pack=pack_u32)

    def _set_soft_min_cclk(self, value: int) -> None:
        self.send_message(0, 0x35, arg=value, pack=pack_u32)

    def _set_soft_max_cclk(self, value: int) -> None:
        self.send_message(0, 0x36, arg=value, pack=pack_u32)
