import logging
import traceback


class requires_paramaters:
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


class log_this:
    def __init__(self, func=None):
        self.func = func

    def __call__(self, *args, **kwargs):
        if not self.func:
            return self.__class__(args[0])

        async def wrapper(*args, **kwargs):
            try:
                result = await self.func(*args, **kwargs)
                return result
            except Exception as e:
                logging.error(f"Error occured in {self.func.__name__} : {e}")
                traceback.print_exc()

        return wrapper(*args, **kwargs)

    @property
    def __name__(self):
        if self.func:
            return self.func.__name__
        return self.__class__.__name__
