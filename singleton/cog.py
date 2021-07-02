from discord.ext import tasks, commands
from asgiref.sync import sync_to_async

from src.utils import loadNearFutureEvents, advertise_event
from singleton.client import Bert


class ReminderCog(commands.Cog):
    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            ReminderCog: The instance
        """
        if ReminderCog.instance is None:
            ReminderCog()
        return ReminderCog.instance

    def __init__(self):
        if ReminderCog.instance is not None:
            raise Exception("This class is a singleton")
        ReminderCog.instance = self

        self.reminders = []
        self.loader.start()
        self.getEvent.start()
        self.pinger.start()
        self.toBePinged = []
        self.near_events = loadNearFutureEvents()

    def cog_unload(self) -> None:
        """Deletes the cog"""
        self.loader.cancel()

    def getLoadedEvents(self) -> list:
        """Returns the loaded events that need to be advertised now

        Returns:
            list: The list of events
        """
        events_to_return = []
        for event in self.near_events:
            if event.isNow:
                events_to_return.append((event, event.guild))
                event.advertised = True
                event.save()
        return events_to_return

    @tasks.loop(seconds=2.0)
    async def pinger(self) -> None:
        """Pings the people targeted by a deathping command"""
        if len(self.toBePinged) != 0:
            await Bert.getInstance().wait_until_ready()
            for pinged, channel in self.toBePinged:
                channel = Bert.getInstance().get_channel(channel)
                await channel.send("{} up".format(pinged))

    @tasks.loop(seconds=2.0)
    async def getEvent(self) -> None:
        """Advertise the current events"""
        events = await sync_to_async(self.getLoadedEvents)()
        for event, guild_id in events:
            guild = Bert.getInstance().get_guild(guild_id)
            await advertise_event(event, guild=guild)

    @tasks.loop(seconds=30.0)
    async def loader(self) -> None:
        """Loads the near events every 30 seconds"""
        self.near_events = await sync_to_async(loadNearFutureEvents)()
