"""SophosXG (SFOS) Firewall support"""
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class SophosSfosSSH(CiscoSSHConnection):
    async def session_preparation(self):
        """Prepare the session after the connection has been established."""
        await asyncio.create_task(self._test_channel_read())
        """
        Sophos Firmware Version SFOS 18.0.0 GA-Build339

        Main Menu

            1.  Network  Configuration
            2.  System   Configuration
            3.  Route    Configuration
            4.  Device Console
            5.  Device Management
            6.  VPN Management
            7.  Shutdown/Reboot Device
            0.  Exit

            Select Menu Number [0-7]:
        """
        self.write_channel("4" + self.RETURN)
        await asyncio.create_task(self._test_channel_read(pattern=r"[console>]"))
        self.set_base_prompt()
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def check_enable_mode(self, *args, **kwargs):
        """No enable mode on SFOS"""
        return True

    def enable(self, *args, **kwargs):
        """No enable mode on SFOS"""
        return ""

    def exit_enable_mode(self, *args, **kwargs):
        """No enable mode on SFOS"""
        return ""

    def check_config_mode(self, *args, **kwargs):
        """No config mode on SFOS"""
        return False

    def config_mode(self, *args, **kwargs):
        """No config mode on SFOS"""
        return ""

    def exit_config_mode(self, *args, **kwargs):
        """No config mode on SFOS"""
        return ""

    def save_config(self, *args, **kwargs):
        """Not Implemented"""
        raise NotImplementedError
