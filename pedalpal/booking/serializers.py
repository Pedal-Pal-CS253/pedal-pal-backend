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


class BookRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ["cycle", "start_time"]


class BookLaterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["cycle", "start_time"]


class EndRideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lock
        fields = ["hub"]

        
class HubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = '__all__'
    