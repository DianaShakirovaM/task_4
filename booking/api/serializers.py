from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import Room, Booking, Amenity, AmenityRoom

User = get_user_model()


class AmnetySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    amenities = AmnetySerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        amenities = validated_data.pop('amenities')
        room = Room.objects.create(**validated_data)

        for amenity in amenities:
            current_amenety, status = Amenity.objects.get_or_create(
                **amenity
            )
            AmenityRoom.objects.create(amenity=current_amenety, room=room)
        return room


class BookingSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(
        input_formats=('%d.%m.%Y %H:%M',),
        format='%d.%m.%Y %H:%M',
    )
    end_time = serializers.DateTimeField(
        input_formats=('%d.%m.%Y %H:%M',),
        format='%d.%m.%Y %H:%M',
    )

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user', 'room')

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError(
                'Время начала должно быть меньше времени окончания.'
            )

        room = self.context.get('room')
        overlapping = Booking.objects.filter(
            room=room,
            end_time__gt=data['start_time'],
            start_time__lt=data['end_time']
        )
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)
        if overlapping.exists():
            raise serializers.ValidationError(
                'Комната уже забронирована на указанное время.'
            )
        return data
