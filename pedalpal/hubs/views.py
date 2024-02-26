from rest_framework import generics,permissions,authentication
from django.http import JsonResponse
from django.db.models import Count,Q

from rest_framework.response import Response

from booking.models import Hub,Cycle
from booking.serializers import CycleSerializer
from .serializers import HubSerializer

class ViewsAPI(generics.GenericAPIView):

    '''
        Uncomment below to authenticate user before viewing hubs.
    '''

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.TokenAuthentication,)


    def get(self, request, *args, **kwargs):
        queryset = Hub.objects.all()
        serializer_class = HubSerializer
        available_cycles = [hub.id for hub in Hub.objects.annotate(num_available=Count('cycle', filter=Q(cycle__booked=False)))]
        hub_data = serializer_class(queryset, many=True).data
        for hub in hub_data:
            hub['available'] = available_cycles[hub_data.index(hub)]
        return JsonResponse(hub_data,safe=False)