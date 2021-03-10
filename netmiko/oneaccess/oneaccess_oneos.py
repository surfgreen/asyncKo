"""Netmiko driver for OneAccess ONEOS"""
from netmiko.cisco_base_connection import CiscoBaseConnection
import asyncio


class OneaccessOneOSBase(CiscoBaseConnection):
    def __init__(self, *args, **kwargs):
        """Init connection - similar as Cisco"""
        default_enter = kwargs.get("default_enter")
        kwargs["default_enter"] = "\r\n" if default_enter is None else default_enter
        super().__init__(*args, **kwargs)

    async def session_preparation(self):
        """Prepare connection - disable paging"""
        await asyncio.create_task(self._test_channel_read())
        self.set_base_prompt()
        self.set_terminal_width(command="stty columns 255", pattern="stty")
        self.disable_paging(command="term len 0")
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def save_config(self, cmd="write mem", confirm=False, confirm_response=""):
        """Save config: write mem"""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )


class OneaccessOneOSSSH(OneaccessOneOSBase):
    pass


class OneaccessOneOSTelnet(OneaccessOneOSBase):
    pass
