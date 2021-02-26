from django.utils import timezone
from discord.ext import tasks, commands
from db.models import Reminder
from asgiref.sync import sync_to_async


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.reminders = []
        self.bot = bot
        self.loader.start()
        self.getEvent.start()
        self.pinger.start()
        self.toBePinged = []
        self.near_events = []

    def cog_unload(self):
        self.loader.cancel()

    def getLoadedEvents(self):
        loadedEvents = self.near_events.filter(start_time__gte=timezone.now())
        events_to_return = []
        for event in loadedEvents:
            if event.isNow:
                events_to_return.append(event)
        return events_to_return

    @tasks.loop(seconds=2.0)
    async def pinger(self):
        if len(self.toBePinged) != 0:
            await self.bot.wait_until_ready()
            for pinged, channel in self.toBePinged:
                channel = self.bot.get_channel(channel)
                await channel.send("{} up".format(pinged))

    @tasks.loop(seconds=2.0)
    async def getEvent(self):
        return await sync_to_async(self.getLoadedEvents)()

    def loadEvents(self):
        """ Loads every event that starts in less than 5 minutes """
        self.near_events = Reminder.objects.filter(
            start_time__gte=timezone.now(),
            start_time__lt=timezone.now() + timezone.timedelta(minutes=5),
        )

    @tasks.loop(seconds=5.0)
    async def loader(self):
        await sync_to_async(self.loadEvents)()
