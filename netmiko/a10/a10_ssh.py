"""A10 support."""
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class A10SSH(CiscoSSHConnection):
    """A10 support."""

    async def session_preparation(self):
        """A10 requires to be enable mode to disable paging."""
        await asyncio.create_task(self._test_channel_read())
        self.set_base_prompt()
        self.enable()

        # Will not do anything without A10 specific command
        # self.set_terminal_width()
        self.disable_paging(command="terminal length 0")

        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def save_config(self, *args, **kwargs):
        """Not Implemented"""
        raise NotImplementedError
