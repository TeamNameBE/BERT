from models.command import Command


class CommandRegistry:
    """Registers bot's available commands"""

    instance = None

    @staticmethod
    def getInstance():
        if CommandRegistry.instance is None:
            CommandRegistry()
        return CommandRegistry.instance

    def __init__(self, func=None):
        if CommandRegistry.instance is not None:
            raise Exception("This class is a singleton")
        CommandRegistry.instance = self

        self.commands = []

    def register(self, *args, **kwargs):
        def decorator(fun):
            command = Command(fun)
            for keyword, value in kwargs.items():
                setattr(command, keyword, value)

            self.commands.append(command)

            async def wrapper(*args, **kwargs):
                await self.func(*args, **kwargs)

            return wrapper
        return decorator

    def get(self, command):
        return self.commands[self.commands.index(command)]
