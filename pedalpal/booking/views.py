import serial
import sys
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import authentication
from django.http.response import JsonResponse

from booking.models import Cycle, Ride, Booking, Lock
from payment.models import Payment
from booking.serializers import (
    BookRideSerializer,
    RideSerializer,
    BookLaterSerializer,
    EndRideSerializer,
)
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils import timezone
from booking.models import Hub, Cycle
from booking.serializers import CycleSerializer
from .serializers import HubSerializer


class BookNowAPI(generics.GenericAPIView):
    serializer_class = BookRideSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cycle = serializer.validated_data.get("cycle")
        user = request.user

        if user.is_ride_active():
            return JsonResponse(
                {"message": "User already has an active ride"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cycle.is_booked():
            if cycle.user == user:
                cycle.book_now(user)
                user.set_ride_active(True)
                booking = Booking.objects.get(user=user, cycle=cycle, end_time=None)
                booking.end_booking(timezone.now())
            else:
                return JsonResponse(
                    {"message": "Cycle already booked"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # arduino1_port = str(cycle.lock.arduino_port)
        # baud_rate = 115200
        # arduino1 = serial.Serial(arduino1_port, baud_rate, timeout=0)
        # val = 1
        # arduino1.write(str(val).encode() + b"\n")

        # received_string = ""
        # flag = 0
        # while received_string == "" and flag < 1000000:
        #     received_string = arduino1.readline().decode().strip()
        #     flag += 1

        # val = 0
        # arduino1.write(str(val).encode() + b"\n")

        # if received_string != "Unlocked":
        #     return JsonResponse(
        #         {"message": "Cycle not unlocked!"}, status=status.HTTP_400_BAD_REQUEST
        #     )

        cycle.book_now(user)
        user.set_ride_active(True)

        start_time = timezone.now()
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
    serializer_class = BookLaterSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        hub = serializer.validated_data.get("hub")
        cycle = Cycle.objects.filter(hub=hub, booked=False, active=False).first()
        start_time = serializer.validated_data.get("start_time")
        user = request.user
        cost = int(
            (start_time - timezone.now()).total_seconds() / 60 * 1 + 1
        )  # 1 rupee per minute

        if not user.is_subscribed:
            return JsonResponse(
                {"message": "You need to be subscribed to avail this service!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.is_ride_active():
            return JsonResponse(
                {"message": "User already has an active ride"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cycle is None:
            return JsonResponse(
                {"message": "Hub does not have any available cycles!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if cycle.is_booked():
            return JsonResponse(
                {"message": "Cycle already booked"}, status=status.HTTP_400_BAD_REQUEST
            )

        if start_time < timezone.now():
            return JsonResponse(
                {"message": "Start time cannot be in the past"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user.balance < cost:
            return JsonResponse(
                {"message": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST
            )

        cycle.book_later(user)

        user.balance -= cost
        user.save()

        payment = Payment.objects.create(user=user, amount=-cost, status="DEBIT")

        booking = Booking.objects.create(
            user=user,
            hub=hub,
            cycle=cycle,
            book_time=timezone.now(),
            start_time=start_time,
            end_time=None,
            cancelled=False,
            cost=cost,
            payment=payment,
        )

        serializer = BookLaterSerializer(booking)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


# TODO: Cancel booking API


class EndRideAPI(generics.GenericAPIView):
    serializer_class = EndRideSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)

    def post(self, request, *args, **kwargs):
        user = request.user

        if user.ride_active is False:
            return JsonResponse(
                {"message": "User does not have an active ride"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ride = Ride.objects.get(user=user, end_time=None)
        id = request.data["id"]
        lock = Lock.objects.get(id=id)
        ride.end_ride(timezone.now(), lock)

        serializer = RideSerializer(ride)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)


class GetHubsDataAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def get(self, request, *args, **kwargs):
        queryset = Hub.objects.all()
        serializer_class = HubSerializer

        available_cycles = Hub.objects.annotate(
            num_available=Count(
                "cycle", filter=Q(cycle__booked=False) & Q(cycle__active=False)
            )
        )

        hub_data = serializer_class(queryset, many=True).data
        for hub in hub_data:
            hub["available"] = available_cycles.get(id=hub["id"]).num_available
        return JsonResponse(hub_data, safe=False)
