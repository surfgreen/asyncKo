"""Alcatel-Lucent Enterprise AOS support (AOS6 and AOS8)."""
import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class AlcatelAosSSH(CiscoSSHConnection):
    """Alcatel-Lucent Enterprise AOS support (AOS6 and AOS8)."""

    async def session_preparation(self):
        # Prompt can be anything, but best practice is to end with > or #
        await asyncio.create_task(self._test_channel_read(pattern=r"[>#]"))
        await asyncio.create_task(self.set_base_prompt())
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def check_enable_mode(self, *args, **kwargs):
        """No enable mode on AOS"""
        pass

    def enable(self, *args, **kwargs):
        """No enable mode on AOS"""
        pass

    def exit_enable_mode(self, *args, **kwargs):
        """No enable mode on AOS"""
        pass

    def check_config_mode(self, *args, **kwargs):
        """No config mode on AOS"""
        pass

    def config_mode(self, *args, **kwargs):
        """No config mode on AOS"""
        return ""

    def exit_config_mode(self, *args, **kwargs):
        """No config mode on AOS"""
        return ""

    def save_config(
        self, cmd="write memory flash-synchro", confirm=False, confirm_response=""
    ):
        """Save Config"""
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )
