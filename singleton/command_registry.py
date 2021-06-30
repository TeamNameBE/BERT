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

    def register(self, function):
        self.commands.append(function)

        async def wrapper(*args, **kwargs):
            print("In register")
            print("*args =", args)
            print("**kwargs =", kwargs)

            await self.func(*args, **kwargs)

        return wrapper()
