"""Extreme Virtual Services Platform Support."""
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class ExtremeVspSSH(CiscoSSHConnection):
    """Extreme Virtual Services Platform Support."""

    async def session_preparation(self):
        """Prepare the session after the connection has been established."""
        await self._test_channel_read()
        self.set_base_prompt()
        self.disable_paging(command="terminal more disable")
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await self.clear_buffer()

    def save_config(self, cmd="save config", confirm=False, confirm_response=""):
        """Save Config"""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )
