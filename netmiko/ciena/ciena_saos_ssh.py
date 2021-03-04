"""Ciena SAOS support."""
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class CienaSaosSSH(CiscoSSHConnection):
    """Ciena SAOS support."""

    async def session_preparation(self):
        await self._test_channel_read()
        self.set_base_prompt()
        self.disable_paging(command="system shell session set more off")
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await self.clear_buffer()

    def enable(self, *args, **kwargs):
        pass

    def save_config(self, *args, **kwargs):
        """Not Implemented"""
        raise NotImplementedError
