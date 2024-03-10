from rest_framework import generics, permissions, authentication, status
from maintenance.models import Feedback
from maintenance.serializers import FeedbackSerializer
from maintenance.permissions import IsAdmin
from django.http.response import JsonResponse


class FeedbackList(generics.ListCreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackAdd(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = FeedbackSerializer

    def post(self, request, *args, **kwargs):
        air_issues = request.data.get("air_issues")
        sound_issues = request.data.get("sound_issues")
        brake_issues = request.data.get("brake_issues")
        chain_issues = request.data.get("chain_issues")
        detailed_issues = request.data.get("detailed_issues")
        user = self.request.user
        feedback = Feedback.objects.create(
            user=user,
            air_issues=air_issues,
            sound_issues=sound_issues,
            brake_issues=brake_issues,
            chain_issues=chain_issues,
            detailed_issues=detailed_issues,
        )
        serialized_feedback = FeedbackSerializer(feedback)
        return JsonResponse(serialized_feedback.data, status=status.HTTP_201_CREATED)
