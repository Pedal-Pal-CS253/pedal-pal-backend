from rest_framework import serializers
from booking.models import Cycle, Ride, Lock, Booking, Hub


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cycle
        fields = "__all__"


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class BookRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lock
        fields = ["id"]


class BookLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["hub", "start_time"]


class EndRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lock
        fields = ["id"]


class HubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = "__all__"
