from singleton.command_registry import CommandRegistry

registry = CommandRegistry.getInstance()


class CommandManager:
    """The singleton responsible of the parsing, loading and execution of commands"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            CommandManager: The instance
        """
        if CommandManager.instance is None:
            CommandManager()
        return CommandManager.instance

    def __init__(self):
        if CommandManager.instance is not None:
            raise Exception("The class is a singleton")
        CommandManager.instance = self

        import src.commands
        import src.slash_commands

    async def execCommand(self, line, channel):
        """Executes the given command if it exists

        Args:
            line (str): The original message content
            channel (discord.channel): The channel in which the command has been done
        """
        parameters = (
            line.replace("\n", " ").replace("\r", " ").replace("\t", " ").split(" ")
        )
        if parameters[0] not in registry.commands:
            await channel.send("Bert pas connaitre `{}`".format(parameters[0]))
            return

        await registry.get(parameters[0])(parameters[1:], channel)
