from models.command import Command


class CommandRegistry:
    """Registers bot's available commands"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            CommandRegistry: The instance
        """
        if CommandRegistry.instance is None:
            CommandRegistry()
        return CommandRegistry.instance

    def __init__(self, func=None):
        if CommandRegistry.instance is not None:
            raise Exception("This class is a singleton")
        CommandRegistry.instance = self

        self.commands = []

    def register(self, *args, **kwargs) -> callable:
        """Decorator used to register a command in the registry, used to list all available commands

        Returns:
            callable: The decorator in itself
        """
        def decorator(fun: callable):
            command = Command(fun)
            for keyword, value in kwargs.items():
                setattr(command, keyword, value)

            self.commands.append(command)

            async def wrapper(*args, **kwargs):
                await self.func(*args, **kwargs)

            return wrapper
        return decorator

    def get(self, command: str) -> callable:
        """Returns the callable corresponding to the given command

        Args:
            command (str): the command

        Returns:
            callable: The function corresponding to the command
        """
        return self.commands[self.commands.index(command)]
