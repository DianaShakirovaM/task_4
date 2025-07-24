from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Amenity(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Удобства'

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField('Название комнаты', max_length=100, unique=True)
    capacity = models.PositiveSmallIntegerField('Вместимость')
    amenities = models.ManyToManyField(
        Amenity, through='AmenityRoom', verbose_name='Удобства'
    )

    def __str__(self):
        return self.name


class AmenityRoom(models.Model):
    amenity = models.ForeignKey(
        Amenity, on_delete=models.CASCADE, verbose_name='Удобства'
    )
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, verbose_name='Команта'
    )


class Booking(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='bookings'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings'
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        ordering = ('start_time',)

    def __str__(self):
        return f'{self.room.name} запронирована {self.user.username}'
