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


@slash.slash(
    name="getfuture",
    description="Shows the event occuring on the given amout of time",
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="time",
            description="the type of time",
            required=False,
            option_type=3,
            choices=[
                create_choice(
                    name="hours",
                    value="hours"
                ),
                create_choice(
                    name="days",
                    value="days"
                ),
                create_choice(
                    name="weeks",
                    value="weeks"
                ),
            ]
        ),
        create_option(
            name="amount",
            description="The quantity of the previously chosen type of time",
            required=False,
            option_type=4
        )
    ]
)
async def _getFuture(ctx: SlashContext, time: str = "weeks", amount: int = 1):
    params = [time, str(amount)]
    command = registry.get("getfuture")
    await command(params, ctx)


@slash.slash(
    name="morsty",
    description="? ? ?",
    guild_ids=constants.guild_ids
)
async def _morsty(ctx: SlashContext):
    command = registry.get("morsty")
    await command([], ctx)


@slash.slash(
    name="pic",
    description=registry.get("pic").description,
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="tag",
            description="A tag for the pic",
            option_type=3,
            required=False
        )
    ]
)
async def _pic(ctx: SlashContext, tag: str = None):
    params = [] if tag is None else [tag]

    command = registry.get("pic")
    await command(params, ctx)


@slash.slash(
    name="vote",
    description=registry.get("vote").description,
    guild_ids=constants.guild_ids,
    options=[
        create_option(
            name="subject",
            description="The subject of the vote",
            option_type=3,
            required=True
        ),
        create_option(
            name="option1",
            description="The option 1",
            option_type=3,
            required=True
        ),
        create_option(
            name="option2",
            description="The option 2",
            option_type=3,
            required=True
        ),
        create_option(
            name="option3",
            description="The option 3",
            option_type=3,
            required=False
        ),
        create_option(
            name="option4",
            description="The option 4",
            option_type=3,
            required=False
        ),
        create_option(
            name="option5",
            description="The option 5",
            option_type=3,
            required=False
        ),
        create_option(
            name="option6",
            description="The option 6",
            option_type=3,
            required=False
        ),
        create_option(
            name="option7",
            description="The option 7",
            option_type=3,
            required=False
        ),
        create_option(
            name="option8",
            description="The option 8",
            option_type=3,
            required=False
        ),
        create_option(
            name="option9",
            description="The option 9",
            option_type=3,
            required=False
        ),
        create_option(
            name="option10",
            description="The option 10",
            option_type=3,
            required=False
        ),
    ]
)
async def _vote(ctx: SlashContext, **kwargs):
    params = [value for key, value in kwargs.items()]
    print(params)

    command = registry.get("vote")
    await command(params, ctx)
