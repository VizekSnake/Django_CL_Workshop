from django.db import models


# Create your models here.
class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField(null=False)
    projector_avaibility = models.BooleanField(default=False)
    additional_info = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.room_name}'


class Reservation(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    reservation_date = models.DateField()
    comment = models.TextField(null=True)

    def __str__(self):
        return f'{self.reservation_date} {self.comment}'

    class Meta:
        unique_together = ('room_id', 'reservation_date',)
