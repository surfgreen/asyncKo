import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class EltexSSH(CiscoSSHConnection):
    async def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        await asyncio.create_task(self._test_channel_read())
        self.set_base_prompt()
        self.disable_paging(command="terminal datadump")

        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def save_config(self, *args, **kwargs):
        """Not Implemented"""
        raise NotImplementedError
