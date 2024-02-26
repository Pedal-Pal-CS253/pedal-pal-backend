from rest_framework import generics,permissions,authentication
from django.http import JsonResponse

from booking.models import Hub
from .serializers import HubSerializer

class ViewsAPI(generics.GenericAPIView):

    '''
        Uncomment below to authenticate user before viewing hubs.
    '''

    # permission_classes = (permissions.IsAuthenticated,)
    # authentication_classes = (authentication.TokenAuthentication,)
    def get(self, request, *args, **kwargs):
        queryset = Hub.objects.all()
        serializer_class = HubSerializer(queryset, many=True)
        return JsonResponse(serializer_class.data,safe=False)