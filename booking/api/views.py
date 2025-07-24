from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.models import Booking, Room
from .permissions import IsAuthorOrReadOnly
from .serializers import RoomSerializer, BookingSerializer


class RoomsViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)

    @action(
        detail=True,
        methods=['get', 'post', 'delete'],
        permission_classes=(IsAuthenticated,)
    )
    def booking(self, request, pk=None):
        room = self.get_object()

        if request.method == 'GET':
            serializer = BookingSerializer(room.bookings.all(), many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = BookingSerializer(
                data=request.data,
                context={'room': room, 'request': request}
            )
            if serializer.is_valid():
                serializer.save(user=request.user, room=room)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
        elif request.method == 'DELETE':
            room.bookings.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def available(self, request):
        """Получение списка свободных комнат на заданный период."""
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not start_time or not end_time:
            return Response(
                {'error': 'Необходимо указать start_time и end_time'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start = datetime.strptime(start_time, '%d.%m.%Y %H:%M')
            end = datetime.strptime(end_time, '%d.%m.%Y %H:%M')
        except ValueError:
            return Response(
                {'error': 'Неверный формат даты.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if start >= end:
            return Response(
                {'error': 'Время начала должно быть раньше времени окончания'},
                status=status.HTTP_400_BAD_REQUEST
            )

        booked_rooms = Booking.objects.filter(
            start_time__lt=end,
            end_time__gt=start
        ).values_list('room_id', flat=True)

        available_rooms = Room.objects.exclude(id__in=booked_rooms)

        serializer = self.get_serializer(available_rooms, many=True)
        return Response(serializer.data)
