from netmiko.cisco_base_connection import CiscoSSHConnection
import asyncio


class DlinkDSBase(CiscoSSHConnection):
    """Supports D-Link DGS/DES device series (there are some DGS/DES devices that are web-only)"""

    async def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        await asyncio.create_task(self._test_channel_read())
        self.set_base_prompt()
        self.disable_paging()
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def disable_paging(self, command="disable clipaging", delay_factor=1):
        return super().disable_paging(command=command, delay_factor=delay_factor)

    def enable(self, *args, **kwargs):
        """No implemented enable mode on D-Link yet"""
        return ""

    def check_enable_mode(self, *args, **kwargs):
        """No implemented enable mode on D-Link yet"""
        return True

    def exit_enable_mode(self, *args, **kwargs):
        """No implemented enable mode on D-Link yet"""
        return ""

    def check_config_mode(self, *args, **kwargs):
        """No config mode on D-Link"""
        return False

    def config_mode(self, *args, **kwargs):
        """No config mode on D-Link"""
        return ""

    def exit_config_mode(self, *args, **kwargs):
        """No config mode on D-Link"""
        return ""

    def save_config(self, cmd="save", confirm=False, confirm_response=""):
        """Saves configuration."""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )

    def cleanup(self):
        """Return paging before disconnect"""
        self.send_command_timing("enable clipaging")
        return super().cleanup()


class DlinkDSSSH(DlinkDSBase):
    pass


class DlinkDSTelnet(DlinkDSBase):
    def __init__(self, *args, **kwargs):
        default_enter = kwargs.get("default_enter")
        kwargs["default_enter"] = "\r\n" if default_enter is None else default_enter
        super().__init__(*args, **kwargs)
