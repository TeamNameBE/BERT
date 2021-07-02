import discord

from datetime import datetime
import datetime as dt
from discord_slash import SlashContext
from django.utils import timezone
from db.models import Reminder

from decorators.log_this import log_this
from singleton.cog import ReminderCog


def createReminder(name: str, start_time, duration, people_to_remind, channel_id, server_id):
    """Creates a reminder object and stores it in the database

    Args:
        name (str): The name of the reminder
        start_time (str): The hour of the start
        duration (str): The duration of the event
        people_to_remind (str): The role/people to remind (@someone)
        channel_id (str): The id of the channel to advertise the reminder in
        server_id (str): The id of the server to advertise the event in
    """
    end_time = start_time + duration
    Reminder.objects.create(
        name=name,
        start_time=start_time,
        end_time=end_time,
        role_to_remind=people_to_remind,
        channel=channel_id,
        guild=server_id,
    )


def modifyReminder(name, server_id, field, value) -> dict:
    """Modifies the selected field of the selected reminer

    Args:
        name (str): The name of the reminder
        server_id (str): The id of the server inn which to modify the reminder
        field (str): The name of the field to modify
        value (str): The new value for the field

    Returns:
        dict: A dictionnary containing the information of wether the modification went well or not
    """
    reminder = Reminder.objects.filter(name=name, guild=server_id)
    if reminder.count() == 0:
        return {"error": True, "msg": f"Bert a pas trouvé événement '{name}'"}

    reminder = reminder.first()

    if field == "start_date":
        try:
            value = datetime.strptime(value, "%d/%m/%Y %H:%M")
        except Exception:
            return {
                "error": True,
                "msg": f"Format pas correct : {value}",
            }
        old_value = datetime.strftime(
            timezone.make_naive(reminder.start_time),
            "%d/%m/%Y %H:%M"
        )
        # Keep the duration constant
        duration = reminder.duration
        reminder.start_time = value
        reminder.set_duration(duration)

    elif field == "name":
        value = value.lower()
        old_value = reminder.name
        reminder.name = value

    elif field == "duration":
        hours, minutes = value.split(":")
        if not hours.isdigit():
            return {"error": True, "msg": "Heures doivent être chiffre"}
        if not minutes.isdigit():
            return {"error": True, "msg": "Minutes doivent être chiffre"}
        duration = dt.timedelta(hours=int(hours), minutes=int(minutes))
        old_value = reminder.duration
        reminder.set_duration(duration)

    elif field == "channel":
        guild = ReminderCog.getInstance().bot.get_guild(server_id)
        channel = guild.get_channel(int(value[2:-1]))
        if channel is None:
            return {"error": True, "msg": f"Bert pas trouvé channel '{value}'"}
        old_value = f"<#{reminder.channel}>"
        reminder.channel = value[2:-1]

    elif field == "allow_dp":
        value = value.lower()
        if value not in ["true", "false"]:
            return {"error": True, "msg": f"Toi choisir 'true' ou 'false', pas {value}"}
        old_value = "true" if reminder.dp_participants else "false"
        reminder.dp_participants = value == "true"

    else:
        return {"error": True, "msg": f"Bert pas connaitre champs {field}"}

    reminder.save()

    return {
        "error": False,
        "msg": f"Bert a modifié champs **{field}** ({old_value} => {value}) événement '**{reminder.name}**'",
    }


def deleteReminder(name: str, server_id: str) -> dict:
    """Delets a reminder in the database

    Args:
        name (str): The name of the reminder to delete
        server_id (str): The id of the server in which to delete the reminder

    Returns:
        dict: A dictionnary containing the information of wether the modification went well or not
    """
    reminder = Reminder.objects.filter(name=name, guild=server_id)
    if reminder.count() == 0:
        return {"error": True, "msg": f"Bert a pas trouvé événement '{name}'"}

    reminder = reminder.first()
    reminder.delete()
    return {"error": False, "msg": f"Bert a supprimé événement '{name}'"}


def getFutureEvents(name: str, value: str, guild: str) -> list:
    """Returns the events in the given period of time from the given server

    Args:
        name (str): the type of timing of the next value (hours, minutes,...)
        value (str): the value of time to get the events in
        guild (str): The id of the guild to get the event in

    Returns:
        list: A list of reminders
    """
    if name == "hours":
        reminders = Reminder.objects.filter(
            start_time__range=[
                timezone.now(),
                timezone.now() + timezone.timedelta(hours=value),
            ]
        ).order_by("start_time")
    elif name == "days":
        reminders = Reminder.objects.filter(
            start_time__range=[
                timezone.now(),
                timezone.now() + timezone.timedelta(days=value),
            ]
        ).order_by("start_time")
    elif name == "week":
        reminders = Reminder.objects.filter(
            start_time__range=[
                timezone.now(),
                timezone.now() + timezone.timedelta(weeks=value),
            ]
        ).order_by("start_time")
    else:
        return Reminder.objects.none()

    reminders = reminders.filter(guild=guild)

    return [reminder.serialized for reminder in reminders]


def loadNearFutureEvents() -> list:
    """Loads every event that starts in less than 5 minutes"""
    return Reminder.objects.filter(
        start_time__gte=timezone.now() - timezone.timedelta(minutes=5),
        start_time__lt=timezone.now() + timezone.timedelta(minutes=5),
        advertised=False,
    )


@log_this
async def advertise_event(event, guild):
    """Displays the event, pinging the people, ...

    Args:
        event (Reminder): The event to advertise
        guild (Discord.Guild): The server on which the event should be advertised
    """
    channel = guild.get_channel(event.channel)
    await channel.send(
        f"Salut {event.role_to_remind} ! C'est le moment pour {event.name} durant {event.duration} !"
    )
    if event.dp_participants:
        await channel.send(f"/deathping {event.role_to_remind}")


@log_this
async def displayResult(channel, result):
    if result["error"]:
        await channel.send(f"**{result['msg']}**")
    else:
        await channel.send(result["msg"])


def _asChannel(channel) -> discord.channel:
    if type(channel) is SlashContext:
        return channel.channel
    return channel
