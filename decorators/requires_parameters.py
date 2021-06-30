class requires_parameters:
    """Indicates that a function requires user arguments"""

    def __init__(self, func=None, nb_parameters=1):
        self.func = func
        self.nb_parameters = nb_parameters

    def __call__(self, *args, **kwargs):
        if not self.func:
            return self.__class__(args[0], nb_parameters=self.nb_parameters)

        async def wrapper(*args, **kwargs):
            if len(args[0]) >= self.nb_parameters:
                await self.func(*args, **kwargs)
            else:
                await args[1].send(
                    f"Ta commande pas correcte, toi taper `/help {self.func.__name__.lower()}` pour plus infos"
                )

        return wrapper(*args, **kwargs)
