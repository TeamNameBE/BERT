from discord.ext import tasks, commands
from asgiref.sync import sync_to_async

from src.utils import loadNearFutureEvents, advertise_event


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.reminders = []
        self.bot = bot
        self.loader.start()
        self.getEvent.start()
        self.pinger.start()
        self.toBePinged = []
        self.near_events = loadNearFutureEvents()

    def cog_unload(self):
        """Deletes the cog"""
        self.loader.cancel()

    def getLoadedEvents(self):
        """Returns the loaded events

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
    async def pinger(self):
        """Pings the people targeted by a deathping command"""
        if len(self.toBePinged) != 0:
            await self.bot.wait_until_ready()
            for pinged, channel in self.toBePinged:
                channel = self.bot.get_channel(channel)
                await channel.send("{} up".format(pinged))

    @tasks.loop(seconds=2.0)
    async def getEvent(self):
        """Loads the next events"""
        events = await sync_to_async(self.getLoadedEvents)()
        for event, guild_id in events:
            guild = self.bot.get_guild(guild_id)
            await advertise_event(event, guild=guild)

    @tasks.loop(seconds=30.0)
    async def loader(self):
        """Loads the near events every 30 seconds"""
        self.near_events = await sync_to_async(loadNearFutureEvents)()
