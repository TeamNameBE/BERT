class Constants:
    instance = None

    @staticmethod
    def getInstance():
        if Constants.instance is None:
            Constants()
        return Constants.instance

    def __init__(self):
        if Constants.instance is not None:
            raise Exception("This class is a singleton")
        Constants.instance = self

        self.guild_ids = [789136699477065748]
