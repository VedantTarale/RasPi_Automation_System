from django.db import models
from django.utils import timezone

# Create your models here.
class Reading(models.Model):

    temperature_data = models.FloatField(null=False)
    pressure_data = models.FloatField(null=False)
    moisture_data = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.temperature_data) +str(self.pressure_data) + str(self.moisture_data)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(Reading, self).save(*args, **kwargs)
