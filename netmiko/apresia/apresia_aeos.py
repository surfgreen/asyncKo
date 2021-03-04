import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class ApresiaAeosBase(CiscoSSHConnection):
    async def session_preparation(self):
        """Prepare the session after the connection has been established."""
        await self._test_channel_read(pattern=r"[>#]")
        self.set_base_prompt()
        self.disable_paging()
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await self.clear_buffer()

    def disable_paging(self, command="", delay_factor=1):
        self.enable()
        check_command = "show running-config | include terminal length 0"
        output = self.send_command(check_command)

        if self.allow_auto_change and "terminal length 0" not in output:
            self.send_config_set("terminal length 0")
        self.exit_enable_mode()


class ApresiaAeosSSH(ApresiaAeosBase):
    pass


class ApresiaAeosTelnet(ApresiaAeosBase):
    def __init__(self, *args, **kwargs):
        default_enter = kwargs.get("default_enter")
        kwargs["default_enter"] = "\r\n" if default_enter is None else default_enter
        super().__init__(*args, **kwargs)
