class Queue1Mixin:
    def q1_0x08(self) -> int | None:
        return self.send_message(1, 0x08)

    def q1_0x10(self) -> int | None:
        return self.send_message(1, 0x10)
