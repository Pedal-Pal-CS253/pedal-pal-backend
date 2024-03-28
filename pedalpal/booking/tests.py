import sys

sys.path.append(".")

from rest_framework.test import APITestCase
from authentication.models import Profile
from authentication.models import ProfileManager
from .models import Hub, Cycle, Lock
from datetime import datetime
from datetime import timedelta


class BookingTestCase(APITestCase):
    def set_up(self):
        profile_manager = ProfileManager()
        profile_manager.model = Profile

        self.user = profile_manager.create_user(
            email="test@test.com",
            password="testpassword",
            first_name="test",
            last_name="user",
            phone="1234567890",
        )

        self.user.is_active = True
        self.user.is_subscribed = True
        self.user.balance = 2000
        self.user.save()

        data = {
            "email": "test@test.com",
            "password": "testpassword",
        }

        self.hub = Hub.objects.create(
            hub_name="Test Hub", max_capacity=10, latitude=0, longitude=0
        )
        self.cycle = Cycle.objects.create(
            hub=self.hub, user=self.user, booked=False, active=False
        )
        self.lock = Lock.objects.create(
            arduino_port="test", hub=self.hub, cycle=self.cycle
        )

        response = self.client.post("/auth/get_auth_token/", data)
        self.token = response.json()["token"]

        self.new_time = datetime.now() + timedelta(minutes=75)

        self.data = {
            "hub": 1,
            "start_time": str(self.new_time),
        }

    def testbl_past_time(self):
        self.set_up()

        new_time = datetime.now() + timedelta(minutes=-20)

        data = {
            "hub": 1,
            "start_time": str(new_time),
        }

        response = self.client.post(
            "/booking/book_later/", data, HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Start time cannot be in the past")

    def testbl_normal(self):
        self.set_up()

        response = self.client.post(
            "/booking/book_later/", self.data, HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, 201)

    def testbl_inactive_user(self):
        self.set_up()

        self.user.is_active = False
        self.user.save()

        response = self.client.post(
            "/booking/book_later/", self.data, HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "User inactive or deleted.")

    def testbl_unsubscribed_user(self):
        self.set_up()

        self.user.is_subscribed = False
        self.user.save()

        response = self.client.post(
            "/booking/book_later/", self.data, HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["message"],
            "You need to be subscribed to avail this service!",
        )

    def testbl_insufficient_balance(self):
        self.set_up()
        self.user.balance = 0
        self.user.save()

        response = self.client.post(
            "/booking/book_later/", self.data, HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["message"], "Insufficient balance")

    def testbl_no_cycle(self):
        self.set_up()

        Cycle.objects.filter(id=self.cycle.id).delete()

        cycles = Cycle.objects.all()
        self.assertEqual(len(cycles), 0)

        response = self.client.post(
            "/booking/book_later/", self.data, HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["message"], "Hub does not have any available cycles!"
        )

    def testbl_cycle_booked(self):
        self.set_up()
        self.cycle.booked = True
        self.cycle.save()

        response = self.client.post(
            "/booking/book_later/", self.data, HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["message"], "Hub does not have any available cycles!"
        )
        # available cycles do not include booked cycles


class ViewHubsTestCase(APITestCase):
    def set_up(self):
        profile_manager = ProfileManager()
        profile_manager.model = Profile

        self.user = profile_manager.create_user(
            email="test@test.com",
            password="testpassword",
            first_name="test",
            last_name="user",
            phone="1234567890",
        )

        self.user.is_active = True
        self.user.is_subscribed = True
        self.user.balance = 2000
        self.user.save()

        data = {
            "email": "test@test.com",
            "password": "testpassword",
        }

        self.hub = Hub.objects.create(
            hub_name="Test Hub 1", max_capacity=10, latitude=0, longitude=0
        )
        self.cycle = Cycle.objects.create(
            hub=self.hub, user=self.user, booked=False, active=False
        )
        self.lock = Lock.objects.create(
            arduino_port="test", hub=self.hub, cycle=self.cycle
        )

        self.hub2 = Hub.objects.create(
            hub_name="Test Hub 2", max_capacity=10, latitude=0, longitude=0
        )
        self.hub3 = Hub.objects.create(
            hub_name="Test Hub 3", max_capacity=10, latitude=0, longitude=0
        )

        response = self.client.post("/auth/get_auth_token/", data)
        self.token = response.json()["token"]

    def test_view_hubs(self):
        self.set_up()

        response = self.client.get(
            "/booking/view_hubs/", HTTP_AUTHORIZATION=f"Token {self.token}"
        )
        API_Data = response.json()
        for id, records in enumerate(API_Data):
            self.assertEqual(records["hub_name"], f"Test Hub {id+1}")

        self.assertEqual(response.status_code, 200)
