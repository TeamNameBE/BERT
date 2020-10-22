import json

from django.db import models


class Reminder(models.Model):
    def __init__(self, time, name, desc):
        self.name = models.CharField(max_length=150)
        self.time = models.DateTimeField(null=True)

    @property
    def isNow(self):
        return False

    @property
    def serialized(self):
        return json.dumps({
            "ID": self.id,
            "Name": self.name,
            "Time": self.time
        })
