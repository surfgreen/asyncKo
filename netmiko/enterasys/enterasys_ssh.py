"""Enterasys support."""
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class EnterasysSSH(CiscoSSHConnection):
    """Enterasys support."""

    async def session_preparation(self):
        """Enterasys requires enable mode to disable paging."""
        await self._test_channel_read()
        self.set_base_prompt()
        self.disable_paging(command="set length 0")
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await self.clear_buffer()

    def save_config(self, *args, **kwargs):
        """Not Implemented"""
        raise NotImplementedError
