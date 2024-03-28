from rest_framework.test import APITestCase
from authentication.models import Profile
from authentication.models import ProfileManager
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from rest_framework import status
from .models import Hub, Cycle, Lock, Ride
import os

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

class BookNowAPITestCase(APITestCase):
    def setUp(self):
        self.hub = Hub.objects.create(
            hub_name="Test Hub",
            max_capacity=10,
            latitude=0,
            longitude=0,
        )
        self.user = Profile.objects.create(
            email="test@user.com",
            first_name="Test",
            last_name="User",
            phone="1234567890",
            password="test1234",
        )
        self.cycle = Cycle.objects.create(hub=self.hub)
        self.lock = Lock.objects.create(
            arduino_port="COM1",
            cycle=self.cycle,
            hub=self.hub,
        )

    def test_book_now(self):
        key = int(os.getenv("SECRET_KEY"))
        id = self.lock.id ^ key
        data = {"id": id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/booking/book/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ride.objects.count(), 1)
        self.cycle.refresh_from_db()
        self.assertTrue(self.cycle.is_booked())
        self.assertTrue(self.cycle.is_active())
        self.assertEqual(self.cycle.user, self.user)
        self.lock.refresh_from_db()
        self.assertFalse(self.lock.cycle)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_ride_active())
        
    def test_no_cycle(self):
        invalid_lock = Lock.objects.create(
            arduino_port="COM2",
            hub=self.hub,
        )
        key = int(os.getenv("SECRET_KEY"))
        id = invalid_lock.id ^ key
        data = {"id": id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/booking/book/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Lock has no cycle attached to it'})
        
    def test_book_ride_with_active_ride(self):
        self.user.set_ride_active(True)
        self.assertTrue(self.user.is_ride_active())
        key = int(os.getenv("SECRET_KEY"))
        id = self.lock.id ^ key
        data = {'id': id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/booking/book/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'User already has an active ride'})

    def test_cycle_already_booked(self):
        other_user = Profile.objects.create(
            email="test2@user",
            first_name="Test2",
            last_name="User",
            phone="1234567890",
        )
        self.cycle.book_now(other_user)
        self.assertTrue(self.cycle.is_booked())
        self.assertFalse(self.user.is_ride_active())
        key = int(os.getenv("SECRET_KEY"))
        id = self.lock.id ^ key
        data = {'id': id}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/booking/book/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Cycle already booked'})


class EndRideAPITestCase(APITestCase):
    def setUp(self):
        self.hub = Hub.objects.create(
            hub_name="Test Hub",
            max_capacity=10,
            latitude=0,
            longitude=0,
        )
        self.user = Profile.objects.create(
            email="test@user.com",
            first_name="Test",
            last_name="User",
            phone="1234567890",
            password="test1234",
        )
        self.user.set_ride_active(True)
        self.cycle = Cycle.objects.create(hub=self.hub)
        self.lock = Lock.objects.create(
            arduino_port="COM1",
            hub=self.hub,
        )
        self.ride = Ride.objects.create(
            user=self.user,
            cycle=self.cycle, 
            start_time=timezone.now(), 
            start_hub=self.hub
        )

    def test_end_ride(self):
        key = int(os.getenv("SECRET_KEY"))
        id = self.lock.id ^ key
        data = {'id': id, 'payment_id' : -1}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/booking/end/", data, format='json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.ride.refresh_from_db()
        self.assertTrue(self.ride.end_time)
        self.cycle.refresh_from_db()
        self.assertFalse(self.cycle.is_active())
        self.lock.refresh_from_db()
        self.assertEqual(self.lock.cycle, self.cycle)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_ride_active())

    def test_no_active_ride(self):
        self.user.set_ride_active(False)
        self.assertFalse(self.user.is_ride_active())
        key = int(os.getenv("SECRET_KEY"))
        id = self.lock.id ^ key
        data = {'id': id, 'payment_id': -1}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/booking/end/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'User does not have an active ride'})
    
    def test_no_lock(self):
        data = {'id': 2, 'payment_id': -1}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/booking/end/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Invalid lock!'})
    
    def test_lock_not_empty(self):
        self.lock.cycle = self.cycle
        self.lock.save()
        key = int(os.getenv("SECRET_KEY"))
        id = self.lock.id ^ key
        data = {'id': id, 'payment_id': -1}
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/booking/end/", data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Lock is not empty!'})
