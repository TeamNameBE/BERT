from django.db import models
from django.utils import timezone


class Reminder(models.Model):
    name = models.CharField(max_length=150, default="none", unique=True)
    start_time = models.DateTimeField(null=True)
    duration = models.TimeField(null=True)
    guild = models.IntegerField(default=0)
    channel = models.IntegerField(default=0)
    role_to_remind = models.TextField(null=True)

    @property
    def isNow(self):
        return timezone.now() >= self.start_time

    @property
    def serialized(self):
        return {
            "ID": self.id,
            "name": self.name,
            "start_time": self.start_time,
            "roles": self.role_to_remind,
            "duration": self.duration,
        }
