from db.models import Reminder
from datetime import datetime
from asgiref.sync import sync_to_async

from src.utils import createReminder



async def addReminder(parameters, channel, cog=None):
    start_time = datetime.strptime(
        "{} {}".format(parameters[0], parameters[1]), "%d/%m/%Y %H:%M"
    )
    name = parameters[2]
    duration = datetime.strptime(parameters[3], "%H:%M")

    await sync_to_async(createReminder)(name, start_time, duration, channel.guild.id)
    await channel.send(
        "Bert a ajouté l'évenement {} le {}".format(
            name, start_time.strftime("%d/%m/%y à %H:%M")
        )
    )


async def delReminder(parameters, channel, cog=None):
    print("delete event")


async def modReminder(parameters, channel, cog=None):
    print("modifying event")

async def deathping(parameters, channel, cog=None):
    print(channel.guild.id)
    uid = parameters[0]
    await channel.send(f"Gonna ping the shit out of {uid}")
    cog.toBePinged.append((uid, channel.id))


async def stopDeathping(parameters, channel, cog=None):
    uid = parameters[0]
    for item in [item for item in cog.toBePinged if uid in item]:
        del cog.toBePinged[cog.toBePinged.index(item)]
        await channel.send(f"Stopping to ping the shit out of {uid}")
        return
    await channel.send(f"{uid} is not in the list of person to deathing")


def getFutureEvents(name, value, cog=None):
    if name == "hours":
        Reminder.objects.filter(
            start_time__range=[
                datetime.now(),
                datetime.now() + datetime.timedelta(hour=value),
            ]
        )
    if name == "days":
        Reminder.objects.filter(
            start_time__range=[
                datetime.now(),
                datetime.now() + datetime.timedelta(day=value),
            ]
        )
    if name == "month":
        Reminder.objects.filter(
            start_time__range=[
                datetime.now(),
                datetime.now() + datetime.timedelta(month=value),
            ]
        )
    if name == "year":
        Reminder.objects.filter(
            start_time__range=[
                datetime.now(),
                datetime.now() + datetime.timedelta(year=value),
            ]
        )


async def getFuture(parameters, channel, cog=None):
    pass


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


async def hjelp(parameters, channel, cog=None):
    await channel.send(
        """```
/addreminder date(jj/mm/yyy) hour(HH:MM) name(no space) duration(HH:MM) peopletoremind(@role)
/delreminder id : deletes a reminder
/modreminder id parameter(nom|start_date|duration) value : modifies a reminder
/getfuture [hour|days|months|year] value : shows the future events until X [days|...]
/help : this message
```""")


commands = {
    "addreminder": addReminder,
    "delreminder": delReminder,
    "modreminder": modReminder,
    "getfuture": getFuture,
    "morsty": morsty,
    "deathping": deathping,
    "stopping": stopDeathping,
    "help": hjelp,
}


async def execCommand(line, channel, cog):
    parameters = line.split(" ")
    if parameters[0] not in commands.keys():
        await channel.send("Bert pas connaitre `{}`".format(parameters[0]))
        return
    else:
        await commands[parameters[0]](parameters[1:], channel, cog)
