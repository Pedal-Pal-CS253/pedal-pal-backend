from rest_framework import generics, permissions
from rest_framework import authentication
from django.http.response import JsonResponse
from booking.models import Ride, Booking
from booking.serializers import RideSerializer, BookingSerializer
from authentication.serializers import BlankUserSerializer, UpdateProfileSerializer


class HistoryViewAPI(generics.GenericAPIView):
    serializer_class = BlankUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def post(self, request):
        rides = Ride.objects.filter(user=request.user)
        serializer = RideSerializer(rides, many=True)
        return JsonResponse(serializer.data, safe=False)


class BookingViewAPI(generics.GenericAPIView):
    serializer_class = BlankUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request):
        user = request.user
        bookings = Booking.objects.filter(user=user)
        serializer = BookingSerializer(bookings, many=True)
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
