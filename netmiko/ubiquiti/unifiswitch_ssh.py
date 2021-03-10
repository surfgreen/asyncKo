import asyncio
from netmiko.ubiquiti.edge_ssh import UbiquitiEdgeSSH


class UbiquitiUnifiSwitchSSH(UbiquitiEdgeSSH):
    async def session_preparation(self):
        """
        Prepare the session after the connection has been established.
        When SSHing to a UniFi switch, the session initially starts at a Linux
        shell. Nothing interesting can be done in this environment, however,
        running `telnet localhost` drops the session to a more familiar
        environment.
        """

        await asyncio.create_task(self._test_channel_read())
        self.set_base_prompt()
        await asyncio.create_task(self.send_command(
            command_string="telnet localhost", expect_string=r"\(UBNT\) >"
        ))
        self.set_base_prompt()
        self.enable()
        self.disable_paging()

        # Clear read buffer
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def cleanup(self, command="exit"):
        """Gracefully exit the SSH session."""
        try:
            # The pattern="" forces use of send_command_timing
            if self.check_config_mode(pattern=""):
                self.exit_config_mode()

            # Exit from the first 'telnet localhost'
            self.write_channel(command + self.RETURN)
        except Exception:
            pass

        super().cleanup()
