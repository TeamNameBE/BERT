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
    params = [name]
    command = registry.get("delreminder")
    await command(params, ctx.channel)
