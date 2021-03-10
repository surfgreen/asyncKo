"""Centec OS Support"""
from netmiko.cisco_base_connection import CiscoBaseConnection
import asyncio


class CentecOSBase(CiscoBaseConnection):
    async def session_preparation(self):
        """Prepare the session after the connection has been established."""
        await asyncio.create_task(self._test_channel_read(pattern=r"[>#]"))
        await asyncio.create_task(self.set_base_prompt())
        self.disable_paging()
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def save_config(self, cmd="write", confirm=False, confirm_response=""):
        """Save config: write"""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )


class CentecOSSSH(CentecOSBase):

    pass


class CentecOSTelnet(CentecOSBase):

    pass
