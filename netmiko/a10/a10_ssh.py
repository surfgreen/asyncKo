"""A10 support."""
import time
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class A10SSH(CiscoSSHConnection):
    """A10 support."""

    async def session_preparation(self):
        """A10 requires to be enable mode to disable paging."""
        self._test_channel_read()
        self.set_base_prompt()
        self.enable()

        # Will not do anything without A10 specific command
        # self.set_terminal_width()
        self.disable_paging(command="terminal length 0")

        # Clear the read buffer
        asyncio.sleep(0.3 * self.global_delay_factor)
        self.clear_buffer()

    def save_config(self, *args, **kwargs):
        """Not Implemented"""
        raise NotImplementedError
