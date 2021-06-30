import discord

from src.cog import ReminderCog
from discord_slash import SlashCommand
from singleton.command_manager import CommandManager


class Bert(discord.Client):
    instance = None

    @staticmethod
    def getInstance():
        if Bert.instance is None:
            Bert()
        return Bert.instance

    def __init__(self):
        if Bert.instance is not None:
            raise Exception("This class is a singleton")

        Bert.instance = self
        super().__init__()

        self.slash = SlashCommand(self, sync_commands=True)
        self.cog = ReminderCog(self)
        self.commandManager = CommandManager(self)

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.content and message.content[0] == "/":
            await self.commandManager.execCommand(message.content[1:], message.channel, self.cog)

    def run(self, token):
        super().run(token)
