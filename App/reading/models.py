from django.db import models
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
# Create your models here.
class Reading(models.Model):
    temperature_data = models.FloatField(null=False)
    pressure_data = models.FloatField(null=False)
    moisture_data = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.temperature_data) +str(self.pressure_data) + str(self.moisture_data)
    
    def to_dict(self):
        # Convert the model instance to a dictionary
        data = {
            'id': self.id,
            'temp': self.temperature_data,
            'pressure': self.pressure_data,
            'moisture': self.moisture_data,
            'time': self.created_at.isoformat(),
        }
        return data
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        super(Reading, self).save(*args, **kwargs)

        channel_layer = get_channel_layer()
        objs = Reading.objects.order_by('-created_at').reverse()[:100]
        data = [reading.to_dict() for reading in objs]
        async_to_sync(channel_layer.group_send)(
            'test_consumer_group', {
                'type':'send_update',
                'value': data
            }
        )
