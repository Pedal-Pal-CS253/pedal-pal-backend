from django.test import TestCase
from .models import Feedback
from rest_framework.test import APITestCase
from authentication.models import Profile



class MaintenanceTestCase(APITestCase):
    def test_maintenance(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "air_issues":True,
            "sound_issues":True,
            "brake_issues":True,
            "chain_issues":False,
            "detailed_issues":"test description",
        }
        response = self.client.post("/maintenance/feedbacks/add/", data)
        print(response.json())
        self.assertEqual(response.status_code, 201)
        
    def setUp(self):
        self.user = Profile.objects.create(
            email="test@user.com",
            first_name="Test",
            last_name="User",
            phone="1234567890",
            password="test1234",
        )

    
