from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from booking.models import Cycle, Ride
from booking.serializers import RideSerializer
from authentication.models import Profile
import datetime


class BookNowAPI(generics.GenericAPIView):
    serializer_class = RideSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        print(request.user)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer)
