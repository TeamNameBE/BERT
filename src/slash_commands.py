import discord

from discord_slash import SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice

from singleton.client import Bert
from singleton.command_registry import CommandRegistry
from singleton.constants import Constants

slash = Bert.getInstance().slash
registry = CommandRegistry.getInstance()
constants = Constants.getInstance()


@slash.slash(
    name="help",
    description="Displays help messages",
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="command",
            description="The command to get help from",
            option_type=3,
            required=False,
            choices=[command.command for command in registry.commands]
        )
    ]
)
async def _help(ctx: SlashContext, command: str = None):
    """Slash command to display help

    Args:
        ctx (SlashContext): The context of the slash command
        command (str, optional): The eventual command to get help on
    """
    help_command = registry.get("help")
    if command is not None:
        await help_command([command], ctx)
    else:
        await help_command([], ctx)


@slash.slash(
    name="addreminder",
    description="creates a reminder at the given date that concerns the mentionned role/user",
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="date",
            description="The date of the reminder",
            required=True,
            option_type=3
        ),
        create_option(
            name="hour",
            description="The hour of the reminder",
            required=True,
            option_type=3
        ),
        create_option(
            name="name",
            description="The name of the reminder",
            required=True,
            option_type=3
        ),
        create_option(
            name="duration",
            description="The duration of the reminder",
            required=True,
            option_type=3
        ),
        create_option(
            name="people_to_remind",
            description="The people concerned by this reminder",
            required=True,
            option_type=3
        )
    ]
)
async def _addreminder(ctx: SlashContext, date: str, hour: str, name: str, duration: str, people_to_remind: str):
    """Slash command to add a reminder

    Args:
        ctx (SlashContext): The context of the slash command
        date (str): The date of the reminder
        hour (str): The hour of the reminder
        name (str): The name of the reminder
        duration (str): theduration of the reminder
        people_to_remind (str): the people to remind
    """
    params = [date, hour, name, duration, people_to_remind]
    command = registry.get("addreminder")
    await command(params, ctx)


@slash.slash(
    name="delreminder",
    description="Deletes a reminder",
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="name",
            description="The name of the reminder",
            required=True,
            option_type=3
        )
    ]
)
async def _delreminder(ctx: SlashContext, name: str):
    """The slash command to delete a reminder

    Args:
        ctx (SlashContext): The context of the slash command
        name (str): the name of the reminder to delete
    """
    params = [name]
    command = registry.get("delreminder")
    await command(params, ctx.channel)


@slash.slash(
    name="modreminder",
    description="Modifies a reminder",
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="name",
            description="The reminder's name",
            required=True,
            option_type=3
        ),
        create_option(
            name="field",
            description="The field to modify",
            required=True,
            option_type=3,
            choices=[
                create_choice(
                    name="start_date",
                    value="date"
                ),
                create_choice(
                    name="name",
                    value="name"
                ),
                create_choice(
                    name="duration",
                    value="duration"
                ),
                create_choice(
                    name="allow_dp",
                    value="allow_dp"
                )
            ]
        ),
        create_option(
            name="value",
            description="The field's new value",
            required=True,
            option_type=3
        )
    ]
)
async def _modReminder(ctx: SlashContext, name: str, field: str, value: str):
    """The slash command to modify a reminder

    Args:
        ctx (SlashContext): The context of the slash command
        name (str): The name of the reminder to modify
        field (str): The field to modify in the reminder
        value (str): The new value for the field
    """
    params = [name, field, value]
    command = registry.get("modreminder")
    await command(params, ctx)


@slash.slash(
    name="deathping",
    description=registry.get("deathping").description,
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="user",
            description="The user to deathping",
            option_type=6,
            required=True
        )
    ]
)
async def _deathping(ctx: SlashContext, user: discord.Member):
    """The slash command to deathping someone

    Args:
        ctx (SlashContext): The context of the slash command
        user (discord.Member): The user to deathping
    """
    params = [user.mention]
    command = registry.get("deathping")
    await command(params, ctx)


@slash.slash(
    name="stopping",
    description=registry.get("stopping").description,
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="user",
            description="The user to stop pinging",
            option_type=6,
            required=True
        )
    ]
)
async def _stopping(ctx: SlashContext, user: discord.Member):
    """The slsh command to stop pinging someone

    Args:
        ctx (SlashContext): The context of the slash command
        user (discord.Member): The user to stop pinging
    """
    params = [user.mention]
    command = registry.get("stopping")
    await command(params, ctx)
