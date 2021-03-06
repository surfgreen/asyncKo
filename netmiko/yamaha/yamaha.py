from netmiko.base_connection import BaseConnection
import asyncio


class YamahaBase(BaseConnection):
    async def session_preparation(self):
        """Prepare the session after the connection has been established."""
        await asyncio.create_task(self._test_channel_read(pattern=r"[>#]"))
        self.set_base_prompt()
        self.disable_paging(command="console lines infinity")
        await asyncio.sleep(0.3 * self.global_delay_factor)
        await asyncio.create_task(self.clear_buffer())

    def check_enable_mode(self, check_string="#"):
        return super().check_enable_mode(check_string=check_string)

    def enable(self, cmd="administrator", pattern=r"Password", **kwargs):
        return super().enable(cmd=cmd, pattern=pattern, **kwargs)

    async def exit_enable_mode(self, exit_command="exit"):
        """
        When any changes have been made, the prompt 'Save new configuration ? (Y/N)'
        appears before exiting. Ignore this by entering 'N'.
        """
        output = ""
        if self.check_enable_mode():
            self.write_channel(self.normalize_cmd(exit_command))
            await asyncio.sleep(1)
            output = self.read_channel()
            if "(Y/N)" in output:
                self.write_channel("N")
            output += self.read_until_prompt()
            if self.check_enable_mode():
                raise ValueError("Failed to exit enable mode.")
        return output

    def check_config_mode(self, check_string="#", pattern=""):
        """Checks if the device is in administrator mode or not."""
        return super().check_config_mode(check_string=check_string, pattern=pattern)

    def config_mode(self, config_command="administrator", pattern="ssword"):
        """Enter into administrator mode and configure device."""
        return self.enable()

    def exit_config_mode(self, exit_config="exit", pattern=">"):
        """
        No action taken. Call 'exit_enable_mode()' to explicitly exit Administration
        Level.
        """
        return ""

    def save_config(self, cmd="save", confirm=False, confirm_response=""):
        """Saves Config."""
        if confirm is True:
            raise ValueError("Yamaha does not support save_config confirmation.")
        self.enable()
        # Some devices are slow so match on trailing-prompt if you can
        return self.send_command(command_string=cmd)


class YamahaSSH(YamahaBase):
    """Yamaha SSH driver."""

    pass


class YamahaTelnet(YamahaBase):
    """Yamaha Telnet driver."""

    pass
