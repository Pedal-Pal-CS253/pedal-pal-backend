from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import authentication
from django.http.response import JsonResponse
from booking.models import Cycle, Ride
from booking.serializers import BookRideSerializer, RideSerializer
import datetime


class BookNowAPI(generics.GenericAPIView):
    serializer_class = BookRideSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cycle = serializer.validated_data.get("cycle")
        user = self.request.user

        if user.is_ride_active():
            return JsonResponse(
                {"message": "User already has an active ride"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cycle.is_booked():
            return JsonResponse(
                {"message": "Cycle already booked"}, status=status.HTTP_400_BAD_REQUEST
            )

        cycle.bookNow(user)
        user.set_ride_active(True)

        start_time = datetime.datetime.now()
        ride = Ride.objects.create(
            user=user,
            cycle=cycle,
            start_time=start_time,
            end_time=None,
            start_hub=cycle.hub,
            end_hub=None,
            time=0,
            payment_id=None,
        )

        serializer = RideSerializer(ride)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class BookLaterAPI(generics.GenericAPIView):
    serializer_class = BookRideSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cycle = serializer.validated_data.get("cycle")
        user = self.request.user

        if cycle.is_booked():
            return JsonResponse(
                {"message": "Cycle already booked"}, status=status.HTTP_400_BAD_REQUEST
            )

        cycle.book(user)

        ride = Ride.objects.create(
            user=user,
            cycle=cycle,
            start_time=serializer.validated_data.get("start_time"),
            end_time=None,
            start_hub=cycle.hub,
            end_hub=None,
            time=0,
            payment_id=None,
        )

        serializer = RideSerializer(ride)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
