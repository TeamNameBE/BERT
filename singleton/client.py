import discord

from discord_slash import SlashCommand
from singleton.command_manager import CommandManager


class Bert(discord.Client):
    """The bot singleton, used to interact with the discord API"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            Bert: The instance
        """
        if Bert.instance is None:
            Bert()
        return Bert.instance

    def __init__(self):
        if Bert.instance is not None:
            raise Exception("This class is a singleton")

        Bert.instance = self
        super().__init__()

        self.slash = SlashCommand(self, sync_commands=True)
        self.commandManager = CommandManager(self)

    async def on_ready(self):
        """Function called when the bot is connected to the API"""
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message: discord.Message):
        """Called when a message is sent womewhere the bot can access

        Args:
            message (discord.Message): The message with its metadata
        """
        if message.content and message.content[0] == "/":
            await self.commandManager.execCommand(message.content[1:], message.channel)
