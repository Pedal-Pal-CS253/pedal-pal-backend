from rest_framework import generics
from maintenance.models import Feedback
from maintenance.serializers import FeedbackSerializer
from maintenance.permissions import IsAdmin


class FeedbackList(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
