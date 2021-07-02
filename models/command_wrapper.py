from discord import Embed


class CommandWrapper:
    """Represents a command, with its help text, its description and the command in itself"""

    def __init__(self, fun: callable):
        self.description = None
        self.command = None
        self.fun = fun
        self.help = ""

    async def __call__(self, *args, **kwargs):
        await self.fun(*args, **kwargs)

    def __str__(self):
        return f"\nCommand: {self.command}\n\tname: {self.fun.__name__}\n\tdescription: {self.description}"

    def __repr__(self):
        return str(self)

    def __eq__(self, command):
        return command == self.command

    def asEmbed(self) -> Embed:
        """Generates an Embed representing the command

        Returns:
            Embed: The embed of the command
        """
        em = Embed(title=self.fun.__name__, description=self.description)
        em.add_field(name="parameters", value=self.help)

        return em

    @property
    def asEmbedPart(self) -> list:
        description = f"**help:**\n {self.help}\n**description:**\n {self.description}"
        return {
            "name": self.fun.__name__,
            "value": description,
            "inline": False
        }
