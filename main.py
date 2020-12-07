import discord
import os
import django

# Django specific settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from src.commands import execCommand
from src.cog import ReminderCog


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        # channel = client.get_channel(776392028598304798)
        # await channel.send('<@&{}> up'.format(389427227785428992))

    async def on_message(self, message):
        # print('Message from {0.author}: {0.content}'.format(message))
        if message.content and message.content[0] == "/":
            await execCommand(message.content[1:], message.channel, cog)


API_KEY = os.environ.get("API_KEY", "")
if API_KEY == "":
    raise Exception("You must specify an API key")

client = MyClient()
cog = ReminderCog(client)

client.run(API_KEY)
