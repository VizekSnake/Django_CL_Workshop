from django.db import models


# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField(null=False)
    projector_avaibility = models.BooleanField(default=False)
    additional_info = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.room_name}'
