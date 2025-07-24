from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

from core.models import Booking


@shared_task
def send_booking_notification(booking_id):
    booking = Booking.objects.get(pk=booking_id)
    message = (
        f'Вы успешно забронировали {booking.room.name}.\n'
        f'Время: с {booking.start_time} до {booking.end_time}.\n'
        f'Вместимость: {booking.room.capacity} человек.\n'
        f'Удобства: {booking.room.amenities or "нет"}.'
    )

    send_mail(
        subject=f'Подтверждение бронирования {booking.room.name}',
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=(booking.user.email,),
        fail_silently=False,
    )
