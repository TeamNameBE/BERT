import json

from django.db import models
from django.utils import timezone


class Reminder(models.Model):
    name = models.CharField(max_length=150, default="none")
    start_time = models.DateTimeField(null=True)
    duration = models.TimeField(null=True)
    role_to_remind = models.CharField(max_length=150, null=True)

    @property
    def isNow(self):
        return timezone.now() >= self.start_time

    @property
    def serialized(self):
        return json.dumps({
            "ID": self.id,
            "Name": self.name,
            "Time": self.time
        })
