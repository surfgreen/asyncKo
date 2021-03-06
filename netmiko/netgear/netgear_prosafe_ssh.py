"""ProSafe OS support"""
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class NetgearProSafeSSH(CiscoSSHConnection):
    """ProSafe OS support"""

    def __init__(self, **kwargs):
        if kwargs.get("default_enter") is None:
            kwargs["default_enter"] = "\r"
        return super().__init__(**kwargs)

    async def session_preparation(self):
        """ProSafe OS requires enabe mode to disable paging."""
        await self._test_channel_read()
        self.set_base_prompt()
        self.enable()
        self.disable_paging(command="terminal length 0")

        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await self.clear_buffer()

    def check_config_mode(self, check_string="(Config)#"):
        return super().check_config_mode(check_string=check_string)

    def config_mode(self, config_command="configure", pattern=r"\)\#"):
        return super().config_mode(config_command=config_command, pattern=pattern)

    def exit_config_mode(self, exit_config="exit", pattern=r"\#"):
        return super().exit_config_mode(exit_config=exit_config, pattern=pattern)

    def save_config(
        self, save_cmd="write memory confirm", confirm=False, confirm_response=""
    ):
        self.enable()
        """ProSafe doesn't allow saving whilst within configuration mode"""
        if self.check_config_mode():
            self.exit_config_mode()

        return super().save_config(
            cmd=save_cmd, confirm=confirm, confirm_response=confirm_response
        )
