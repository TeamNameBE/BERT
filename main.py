import discord
import os

from src.commands import execCommand


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        # channel = client.get_channel(755154529401438344)
        # await channel.send('Hello')

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if message.content and message.content[0] == "/":
            await execCommand(message.content[1:], message.channel)


API_KEY = os.environ.get("API_KEY", "")
if API_KEY == "":
    raise Exception("You must specify an API key")

client = MyClient()
client.run(API_KEY)
