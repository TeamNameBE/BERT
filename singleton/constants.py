class Constants:
    """The singleton registering the constant"""

    instance = None

    @staticmethod
    def getInstance():
        """Returns the instance of the singleton

        Returns:
            Constants: The instance
        """
        if Constants.instance is None:
            Constants()
        return Constants.instance

    def __init__(self):
        if Constants.instance is not None:
            raise Exception("This class is a singleton")
        Constants.instance = self

        self.guild_ids = [789136699477065748]
        self.deathping_gif = "https://tenor.com/bih59.gif"
