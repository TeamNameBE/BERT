import discord
import os


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        # channel = client.get_channel(755154529401438344)
        # await channel.send('Hello')

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        if str(message.author) != "Bert#4668":
            await message.channel.send('Lu')


API_KEY = os.environ.get("API_KEY", "")
if API_KEY == "":
    raise Exception("You must specify an API key")

client = MyClient()
client.run(API_KEY)
