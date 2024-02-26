from rest_framework import generics, permissions
from rest_framework import authentication
from django.http.response import JsonResponse
from booking.models import Ride
from booking.serializers import RideSerializer


class HistoryViewAPI(generics.ListCreateAPIView):
    serializer_class = RideSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self, request):
        rides = Ride.objects.filter(user=self.request.user)
        serializer = RideSerializer(rides, many=True)
        return JsonResponse(serializer.data, safe=False)
