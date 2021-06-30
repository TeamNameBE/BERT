class Command:
    def __init__(self, fun):
        self.description = None
        self.command = None
        self.fun = fun

    async def __call__(self, *args, **kwargs):
        await self.fun(*args, **kwargs)

    def __str__(self):
        return f"\nCommand: {self.command}\n\tname: {self.fun.__name__}\n\tdescription: {self.description}"

    def __repr__(self):
        return str(self)

    def __eq__(self, command):
        return command == self.command
