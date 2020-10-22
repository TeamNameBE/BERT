from discord.ext import tasks, commands


class ReminderCog(commands.Cog):
    def __init__(self, bot):
        self.reminders = []
        self.bot = bot
        self.loader.start()

    def cog_unload(self):
        self.loader.cancel()

    def getEvent(self):
        pass

    @tasks.loop(minutes=30.0)
    async def loader(self):
        print("been called")
