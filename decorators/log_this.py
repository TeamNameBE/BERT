from datetime import datetime
import logging
import traceback


class log_this:
    """Handles the logging of eventual exceptions"""

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
                timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                logging.error(
                    f"\n\n*** {timestamp} ***\nError occured in {self.func.__name__} : {e}")
                traceback.print_exc()

        return wrapper(*args, **kwargs)

    @property
    def __name__(self):
        if self.func:
            return self.func.__name__
        return self.__class__.__name__
