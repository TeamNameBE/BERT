from singleton.command_registry import CommandRegistry

registry = CommandRegistry.getInstance()


class CommandManager:
    instance = None

    @staticmethod
    def getInstance():
        if CommandManager.instance is None:
            CommandManager()
        return CommandManager.instance

    def __init__(self, client):
        if CommandManager.instance is not None:
            raise Exception("The class is a singleton")
        CommandManager.instance = self

        import src.commands
        import src.slash_commands

        self.client = client

    async def execCommand(self, line, channel, cog):
        """Executes the given command if it exists

        Args:
            line (str): The original message content
            channel (discord.channel): The channel in which the command has been done
            cog (Cog): The cog which handles the periodic events.
        """
        parameters = (
            line.replace("\n", " ").replace("\r", " ").replace("\t", " ").split(" ")
        )
        if parameters[0] not in registry.commands:
            await channel.send("Bert pas connaitre `{}`".format(parameters[0]))
            return

        print("Searching for", parameters[0])
        print(registry.get(parameters[0]))
        await registry.get(parameters[0])(parameters[1:], channel, cog)
