import requests
import emoji

from datetime import datetime
import datetime as dt

import discord
from discord import Embed

from django.utils import timezone
from asgiref.sync import sync_to_async

from src.utils import (
    createReminder, deleteReminder, getFutureEvents, modifyReminder, displayResult, _asChannel as _, parseVote)
from src.settings import UNSPLASH_API
from decorators.log_this import log_this
from decorators.requires_parameters import requires_parameters
from exceptions.bad_format_exception import BadFormatException
from singleton.command_registry import CommandRegistry
from singleton.cog import ReminderCog
from singleton.constants import Constants

registry = CommandRegistry.getInstance()
constants = Constants.getInstance()


@requires_parameters(nb_parameters=5)
@log_this
@registry.register(
    command="addreminder",
    description="Adds a reminder",
    help="date(jj/mm/yyyy) hour(HH:MM) name(no space) duration(HH:MM) peopletoremind(@role)"
)
async def addReminder(parameters, channel):
    """Adds a reminder in the database

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
    try:
        start_time = datetime.strptime(
            "{} {}".format(parameters[0], parameters[1]), "%d/%m/%Y %H:%M"
        )
        name = parameters[2].lower()

        hours, minutes = parameters[3].split(":")
        duration = dt.timedelta(hours=int(hours), minutes=int(minutes))
    except ValueError as e:
        await channel.send("Valeur pas valide :", e)
        return

    people_to_remind = " ".join(parameters[4:])

    start_time = timezone.make_aware(start_time)

    await sync_to_async(createReminder)(
        name=name,
        start_time=start_time,
        duration=duration,
        people_to_remind=people_to_remind,
        channel_id=_(channel).id,
        server_id=_(channel).guild.id,
    )
    message = "Bert a ajouté l'évenement **{}** le **{}** (pour {})".format(
        name, start_time.strftime("%d/%m/%Y à %H:%M"), people_to_remind
    )
    await channel.send(message)


@requires_parameters
@log_this
@registry.register(
    command="delreminder",
    description="Deletes a reminder",
    help="name"
)
async def delReminder(parameters, channel):
    """Deletes a reminder

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
    name = parameters[0]

    guild_id = _(channel).guild.id
    result = await sync_to_async(deleteReminder)(name, guild_id)
    await displayResult(channel, result)


@requires_parameters(nb_parameters=3)
@log_this
@registry.register(
    command="modreminder",
    description="Modifies a field of a reminder",
    help="name parameter(name|start_date|duration|channel|allow_dp) new_value"
)
async def modReminder(parameters, channel):
    """Modifies the selected field from a reminder

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
    name = parameters[0]
    guild_id = _(channel).guild.id
    field = parameters[1]
    value = " ".join(parameters[2:])

    result = await sync_to_async(modifyReminder)(
        name=name, server_id=guild_id, field=field, value=value
    )
    await displayResult(channel, result)


@requires_parameters
@log_this
@registry.register(
    command="deathping",
    description="Pings a person every two seconds until stopped",
    help="[@someone]"
)
async def deathping(parameters, channel):
    """Launches a deathping on the given user (The bot will ping the user every two seconds)

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
    uids = parameters
    for uid in uids:
        if uid.startswith("<") and uid.endswith(">"):
            ReminderCog.getInstance().toBePinged.append((uid, _(channel).id))
            await channel.send(f"Gonna ping the shit out of {uid}\n{constants.deathping_gif}")


@requires_parameters
@log_this
@registry.register(
    command="stopping",
    description="Stops pinging a person",
    help="[@someone]"
)
async def stopping(parameters, channel):
    """Stops the deathping on the selected user

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
    uids = parameters
    cog = ReminderCog.getInstance()
    for uid in uids:
        uid = uid.replace("!", "")
        if uid.startswith("<") and uid.endswith(">"):
            if (uid, _(channel).id) in cog.toBePinged:
                del cog.toBePinged[cog.toBePinged.index((uid, _(channel).id))]
                await channel.send(f"Stopping to ping the shit out of {uid}")
            else:
                await channel.send(
                    f"{uid} is not in the list of person to deathing in this channel"
                )


@log_this
@registry.register(
    command="getfuture",
    description="Shows a list of future reminders",
    help="[hours|days|weeks] value"
)
async def getFuture(parameters, channel):
    """Returns the future events occuring in the given period of time

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
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
        name=field, value=value, guild=_(channel).guild.id
    )
    for event in future_events:
        await channel.send(
            f"```Événement : {event['name']}\n  Début : {event['start_time']}\n  Durée : {event['duration']}\n\n```"
        )
    if len(future_events) == 0:
        await channel.send("Bert a pas trouvé événements dans période donnée")


@log_this
@registry.register(
    command="morsty",
    description="? ? ?",
    help="? ? ?"
)
async def morsty(_parameters, channel):
    """Morsty's a mystery"""
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
@registry.register(
    command="help",
    description="Prints help messages",
    help="[command]"
)
async def hjelp(parameters, channel):
    """Displays help messages on the commands

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
    if len(parameters) >= 1:
        for command in parameters:
            if (commandWrapper := registry.get(command)) is not None:
                await channel.send(embed=commandWrapper.asEmbed())
            else:
                await channel.send(f"Commande '{command}' pas dans aide de bert")
    else:
        help_msg = Embed(title="Help", description="Help for the functions")
        for command in registry.commands:
            help_msg.add_field(**command.asEmbedPart)
        await channel.send(embed=help_msg)


@requires_parameters
@log_this
@registry.register(
    command="pic",
    description="Shows a random image with the given tags",
    help="[tag]"
)
async def pic(parameters, channel):
    """Shows a random pic using the given tag

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
    query = " ".join(parameters)
    payload = {"client_id": UNSPLASH_API, "query": query}
    response = requests.get("https://api.unsplash.com/photos/random", params=payload)

    response = response.json()

    author = response['user']['name']
    author_url = f"https://unsplash.com/@{response['user']['username']}?utm_source=Bert&utm_medium=referral"
    unsplash_url = "https://unsplash.com/?utm_source=Bert&utm_medium=referral"

    em = discord.Embed(
        title=response["alt_description"],
        description=f"Picture by [{author}]({author_url}) on [Unsplash]({unsplash_url})",
    )
    em.set_image(url=response["urls"]["small"])
    em.set_author(
        name=response["user"]["name"],
        url=f"https://unsplash.com/@{response['user']['username']}?utm_source=Bert&utm_medium=referral",
    )
    await channel.send(embed=em)


@requires_parameters
@log_this
@registry.register(
    command="vote",
    description="Proposes a vote with the given options",
    help="\"Question\" \"proposition 0\" ... \"proposition 10\""
)
async def vote(parameters, channel):
    """Creates a vote embed

    Args:
        parameters (list): The list of parameters required for the command to work
        channel (discord.channel): The channel in which the command has been done
    """
    word_num = [
        "zero", "one", "two", "three", "four",
        "five", "six", "seven", "eight", "nine",
    ]
    word_emojis = [f":keycap_{x}:" for x in range(10)]

    try:
        parsed = parseVote(parameters, not type(channel) is discord.channel)
    except BadFormatException as e:
        await channel.send(str(e))
        return

    question = parsed[0]
    responses = parsed[1:]

    em = discord.Embed(
        title=question,
        description="React to this message to vote",
    )

    for i, response in enumerate(responses):
        em.add_field(name=response, value=f":{word_num[i]}:")

    message = await channel.send(embed=em)

    for i in range(len(responses)):
        await message.add_reaction(emoji.emojize(word_emojis[i]))
