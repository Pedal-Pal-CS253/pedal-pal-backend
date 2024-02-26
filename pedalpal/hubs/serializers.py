from booking.models import Hub
from rest_framework import serializers

class HubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hub
        fields = '__all__'