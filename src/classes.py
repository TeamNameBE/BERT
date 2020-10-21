import json


class Reminder(object):
    def __init__(self, time, name, desc):
        self.id = None
        self.name = name
        self.time = time
        self.desc = desc

    def isNow(self):
        return False

    @property
    def serialized(self):
        return json.dumps({
            "ID": self.id,
            "Name": self.name,
            "Time": self.time,
            "Desc": self.desc}
        )
