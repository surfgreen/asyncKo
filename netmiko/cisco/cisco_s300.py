import asyncio
from netmiko.cisco_base_connection import CiscoSSHConnection


class CiscoS300SSH(CiscoSSHConnection):
    """
    Support for Cisco SG300 series of devices.

    Note, must configure the following to disable SG300 from prompting for username twice:

    configure terminal
    ip ssh password-auth
    """

    async def session_preparation(self):
        """Prepare the session after the connection has been established."""
        self.ansi_escape_codes = True
        await asyncio.create_task(self._test_channel_read())
        self.set_base_prompt()
        self.set_terminal_width(command="terminal width 511", pattern="terminal")
        self.disable_paging(command="terminal datadump")
        # Clear the read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)

    def save_config(self, cmd="write memory", confirm=True, confirm_response="Y"):
        return super().save_config(
            cmd=cmd, confirm=confirm, confirm_response=confirm_response
        )
