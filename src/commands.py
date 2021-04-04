import json
from datetime import datetime
import requests
import discord
import emoji
import re

from django.utils import timezone
from django.contrib.humanize.templatetags.humanize import naturaltime
from asgiref.sync import sync_to_async

from src.utils import createReminder, deleteReminder, getFutureEvents, modifyReminder
from src.decorators import requires_paramaters, log_this
from settings import UNSPLASH_API


@log_this
async def displayResult(channel, result):
    if result["error"]:
        await channel.send(f"**{result['msg']}**")
    else:
        await channel.send(result["msg"])


@requires_paramaters(nb_parameters=5)
@log_this
async def addReminder(parameters, channel, cog=None):
    start_time = datetime.strptime(
        "{} {}".format(parameters[0], parameters[1]), "%d/%m/%Y %H:%M"
    )
    name = parameters[2].lower()
    duration = datetime.strptime(parameters[3], "%H:%M")
    people_to_remind = " ".join(parameters[4:])

    await sync_to_async(createReminder)(
        name=name,
        start_time=start_time,
        duration=duration,
        people_to_remind=people_to_remind,
        channel_id=channel.id,
        server_id=channel.guild.id,
    )
    message = "Bert a ajouté l'évenement **{}** le **{}** (pour {})".format(
        name, start_time.strftime("%d/%m/%y à %H:%M"), people_to_remind
    )
    await channel.send(message)


@requires_paramaters
@log_this
async def delReminder(parameters, channel, cog=None):
    name = parameters[0]

    result = await sync_to_async(deleteReminder)(name, channel.guild.id)
    await displayResult(channel, result)


@requires_paramaters(nb_parameters=3)
@log_this
async def modReminder(parameters, channel, cog=None):
    name = parameters[0]
    guild_id = channel.guild.id
    field = parameters[1]
    value = " ".join(parameters[2:])

    result = await sync_to_async(modifyReminder)(
        name=name, server_id=guild_id, field=field, value=value, cog=cog
    )
    await displayResult(channel, result)


@requires_paramaters
@log_this
async def deathping(parameters, channel, cog=None):
    uids = parameters
    for uid in uids:
        if uid.startswith("<") and uid.endswith(">"):
            settings = json.load(open("settings.json"))

            await channel.send(f"Gonna ping the shit out of {uid}")
            await channel.send(settings["constants"]["deathping_gif"])
            cog.toBePinged.append((uid, channel.id))


@requires_paramaters
@log_this
async def stopping(parameters, channel, cog=None):
    uids = parameters
    for uid in uids:
        if uid.startswith("<") and uid.endswith(">"):
            if (uid, channel.id) in cog.toBePinged:
                del cog.toBePinged[cog.toBePinged.index((uid, channel.id))]
                await channel.send(f"Stopping to ping the shit out of {uid}")
            else:
                await channel.send(
                    f"{uid} is not in the list of person to deathing in this channel"
                )


@log_this
async def getFuture(parameters, channel, cog=None):
    if len(parameters) == 0:
        field = "days"
        value = "7"
    else:
        field = parameters[0]
        value = parameters[1]
    if not value.isdigit():
        await channel.send(f"La valeur {value} doit être chiffre")
        return
    value = int(value)
    future_events = await sync_to_async(getFutureEvents)(
        name=field, value=value, guild=channel.guild.id
    )
    for event in future_events:
        await channel.send(
            f"```Événement : {event['name']}\n  Début : {event['start_time']}\n  Durée : {event['duration']}\n\n \
                {naturaltime(event['start_time'])}```"
        )
    if len(future_events) == 0:
        await channel.send("Bert a pas trouvé événements dans période donnée")


@log_this
async def morsty(parameters, channel, cog=None):
    await channel.send(
        """```
               ___
            .-9 9 `\\     Is it
          =(:(::)=  ;       Binary ?
   Who      ||||     \\
     am     ||||      `-.
    I ?    ,\\|\\|         `,
          /                \\    What's life ?
         ;                  `'---.,
         |                         `\\
         ;                     /     |
 Is it   \\                    |      /
 morse ?  )           \\  __,.--\\    /
       .-' \\,..._\\     \\`   .-'  .-'
      `-=``      `:    |   /-/-/`
                   `.__/
```"""
    )


@log_this
async def hjelp(parameters, channel, cog=None):
    settings = json.load(open("settings.json"))

    if len(parameters) >= 1:
        for command in parameters:
            command = f"/{command}"
            if command in settings["help"].keys():
                await channel.send(f"```{command}: {settings['help'][command]}```")
            else:
                await channel.send(f"Commande '{command}' pas dans aide de bert")
    else:
        help_msg = "```"
        for command, help_text in settings["help"].items():
            help_msg += f"{command}: {help_text}\n\n"
        help_msg += "```"
        await channel.send(help_msg)


@requires_paramaters
@log_this
async def pic(parameters, channel, cog=None):
    category = parameters[0]
    payload = {"client_id": UNSPLASH_API, "query": category}
    response = requests.get("https://api.unsplash.com/photos/random", params=payload)
    response = response.json()
    em = discord.Embed(
        title=response["alt_description"],
        description=f"Picture by [{response['user']['name']}](https://unsplash.com/@{response['user']['username']}?utm_source=Bert&utm_medium=referral) on [Unsplash](https://unsplash.com/?utm_source=Bert&utm_medium=referral)",
    )
    em.set_image(url=response["urls"]["small"])
    em.set_author(
        name=response["user"]["name"],
        url=f"https://unsplash.com/@{response['user']['username']}?utm_source=Bert&utm_medium=referral",
    )
    await channel.send(embed=em)


@requires_paramaters
@log_this
async def vote(parameters, channel, cog=None):
    word_num = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    word_emojis = [f":keycap_{x}:" for x in range(10)]

    parameters = " ".join(parameters)
    vote_regex = "^\"([a-zA-Z0-9?!'éèàù ])+\"( \"([a-zA-Z0-9?!'éèàù ])+\"){1,10}$"

    if not re.match(vote_regex, parameters):
        await channel.send(
            "Commande pas correcte, doit convenir à\n```re\n{}```\n(Exemple) : `{}`".format(
                vote_regex,
                "/vote \"Ca va ?\" \"Oui\" \"Non\""))
        return

    splitted = re.findall(r'"(.*?)"', parameters)
    question = splitted[0]
    responses = splitted[1:]
    print(responses)

    em = discord.Embed(
        title=question,
        description="React to this message to vote",
    )

    print(len(responses))
    for i in range(len(responses)):
        em.add_field(name=responses[i], value=f":{word_num[i]}:")

    message = await channel.send(embed=em)

    for i in range(len(responses)):
        await message.add_reaction(emoji.emojize(word_emojis[i]))


commands = {
    "addreminder": addReminder,
    "delreminder": delReminder,
    "modreminder": modReminder,
    "getfuture": getFuture,
    "morsty": morsty,
    "deathping": deathping,
    "stopping": stopping,
    "help": hjelp,
    "pic": pic,
    "vote": vote
}


@log_this
async def execCommand(line, channel, cog):
    parameters = (
        line.replace("\n", " ").replace("\r", " ").replace("\t", " ").split(" ")
    )
    if parameters[0] not in commands.keys():
        await channel.send("Bert pas connaitre `{}`".format(parameters[0]))
        return
    else:
        await commands[parameters[0]](parameters[1:], channel, cog)
