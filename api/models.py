from django.utils import timezone
from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.

class Snapshot(models.Model):
    timestamp = models.DateTimeField()
    stations = JSONField()
    weather = JSONField()

    def __str__(self):
        if not self.id:
            return 'Unsaved timestamp'
        else:
            return datetime.strftime(self.timestamp, '%Y-%m-%d:T%X')

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = timezone.now()
        return super(Snapshot, self).save(*args, **kwargs)
