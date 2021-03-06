import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class AccedianSSH(CiscoSSHConnection):
    async def session_preparation(self):
        await self._test_channel_read()
        self.set_base_prompt()
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await self.clear_buffer()

    def check_enable_mode(self, *args, **kwargs):
        raise AttributeError("Accedian devices do not support enable mode!")

    def enable(self, *args, **kwargs):
        raise AttributeError("Accedian devices do not support enable mode!")

    def exit_enable_mode(self, *args, **kwargs):
        raise AttributeError("Accedian devices do not support enable mode!")

    def check_config_mode(self):
        """Accedian devices do not have a config mode."""
        return False

    def config_mode(self):
        """Accedian devices do not have a config mode."""
        return ""

    def exit_config_mode(self):
        """Accedian devices do not have a config mode."""
        return ""

    def set_base_prompt(
        self, pri_prompt_terminator=":", alt_prompt_terminator="#", delay_factor=2
    ):
        """Sets self.base_prompt: used as delimiter for stripping of trailing prompt in output."""
        super().set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor,
        )
        return self.base_prompt

    def save_config(self, *args, **kwargs):
        """Not Implemented"""
        raise NotImplementedError
