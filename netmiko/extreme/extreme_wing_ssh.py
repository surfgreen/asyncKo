import time
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class ExtremeWingSSH(CiscoSSHConnection):
    """Extreme WiNG support."""

    async def session_preparation(self):
        """Disable paging and set Max term width"""
        self._test_channel_read(pattern=r">|#")
        self.set_base_prompt()
        self.set_terminal_width(command="terminal width 512", pattern="terminal")
        self.disable_paging(command="no page")
        await asyncio.sleep(0.3 * self.global_delay_factor)
        self.clear_buffer()
