from decorators.log_this import log_this
from decorators.requires_parameters import requires_paramaters

import datetime
from datetime import datetime as dt

from django.utils import timezone
from asgiref.sync import sync_to_async

from src.utils import createReminder

from singleton.command_registry import CommandRegistry

registry = CommandRegistry.getInstance()


class CommandManager:
    instance = None
    commands = []

    @staticmethod
    def getInstance():
        if CommandManager.instance is None:
            CommandManager()
        return CommandManager.instance

    def __init__(self, client):
        if CommandManager.instance is not None:
            raise Exception("The class is a singleton")
        CommandManager.instance = self

        self.client = client

    @log_this
    async def execCommand(self, line, channel, cog):
        """Executes the given command if it exists

        Args:
            line (str): The original message content
            channel (discord.channel): The channel in which the command has been done
            cog (Cog): The cog which handles the periodic events.
        """
        print(self.commands)
        parameters = (
            line.replace("\n", " ").replace("\r", " ").replace("\t", " ").split(" ")
        )
        if parameters[0] not in self.commands.keys():
            await channel.send("Bert pas connaitre `{}`".format(parameters[0]))
            return
        await self.commands[parameters[0]](parameters[1:], channel, cog)

    @requires_paramaters(nb_parameters=5)
    @log_this
    @registry.register
    async def addReminder(self, parameters, channel, cog=None):
        """Adds a reminder in the database

        Args:
            parameters (list): The list of parameters required for the command to work
            channel (discord.channel): The channel in which the command has been done
            cog (Cog, optional): The cog which handles the periodic events. Defaults to None.
        """
        start_time = datetime.strptime(
            "{} {}".format(parameters[0], parameters[1]), "%d/%m/%Y %H:%M"
        )
        name = parameters[2].lower()

        hours, minutes = parameters[3].split(":")
        duration = dt.timedelta(hours=int(hours), minutes=int(minutes))

        people_to_remind = " ".join(parameters[4:])

        start_time = timezone.make_aware(start_time)

        await sync_to_async(createReminder)(
            name=name,
            start_time=start_time,
            duration=duration,
            people_to_remind=people_to_remind,
            channel_id=channel.id,
            server_id=channel.guild.id,
        )
        message = "Bert a ajouté l'évenement **{}** le **{}** (pour {})".format(
            name, start_time.strftime("%d/%m/%Y à %H:%M"), people_to_remind
        )
        await channel.send(message)
