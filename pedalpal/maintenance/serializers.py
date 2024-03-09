from rest_framework import serializers
from maintenance.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            "user",
            "air_issues",
            "sound_issues",
            "brake_issues",
            "chain_issues",
            "detailed_issues",
        ]
