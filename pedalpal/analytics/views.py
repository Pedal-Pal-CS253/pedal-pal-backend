from rest_framework import generics, permissions
from rest_framework import authentication
from django.http.response import JsonResponse
from booking.models import Ride
from booking.serializers import RideSerializer
from authentication.serializers import BlankUserSerializer


class HistoryViewAPI(generics.GenericAPIView):
    serializer_class = BlankUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        rides = Ride.objects.filter(user=request.user)
        serializer = RideSerializer(rides, many=True)
        return JsonResponse(serializer.data, safe=False)
