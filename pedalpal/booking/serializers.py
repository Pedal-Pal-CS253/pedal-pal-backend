from rest_framework import serializers
from booking.models import Cycle, Ride


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
