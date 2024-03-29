import pytz

from django.db import models
from django.utils import timezone


class Reminder(models.Model):
    """The reminder objects used to retain reminder informations, dates etc"""

    name = models.CharField(max_length=150, default="none", unique=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    guild = models.PositiveBigIntegerField(default=0)
    channel = models.PositiveBigIntegerField(default=0)
    role_to_remind = models.TextField(null=True)
    advertised = models.BooleanField(default=False)
    dp_participants = models.BooleanField(default=False)

    @property
    def isNow(self) -> bool:
        """Whether the event should be advertised now or not

        Returns:
            bool: Whether the event should be advertised
        """
        return (timezone.now() >= self.start_time) and not self.advertised

    @property
    def duration(self) -> int:
        """Returns the duration of the event

        Returns:
            int: The duration of the event
        """
        return self.end_time - self.start_time

    @property
    def serialized(self) -> dict:
        """Returns a serialized version of the event

        Returns:
            dict: The event serialized
        """
        return {
            "ID": self.id,
            "name": self.name,
            "start_time": self.start_time.astimezone(pytz.timezone('Europe/Brussels')).strftime("%d %b %Y à %H:%M"),
            "roles": self.role_to_remind,
            "duration": self.duration,
        }

    def set_duration(self, duration):
        """Sets the duration of a reminder by moving the end_time

        Args:
            duration (int): The duration of the event
        """
        self.end_time = self.start_time + duration

    def __repr__(self):
        return f"Reminder {self.name} (advertised: {self.advertised})"
