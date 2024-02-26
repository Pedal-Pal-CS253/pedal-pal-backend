from rest_framework import generics, permissions
from rest_framework import authentication
from django.http.response import JsonResponse
from booking.models import Ride
from authentication.models import Profile
from booking.serializers import RideSerializer
from authentication.serializers import BlankUserSerializer, UpdateProfileSerializer


class HistoryViewAPI(generics.GenericAPIView):
    serializer_class = BlankUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        rides = Ride.objects.filter(user=request.user)
        serializer = RideSerializer(rides, many=True)
        return JsonResponse(serializer.data, safe=False)


class UserUpdateAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, status=400)
