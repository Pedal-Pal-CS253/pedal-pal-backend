from rest_framework import status
from rest_framework.test import APITestCase
from .models import Hub, Cycle, Lock, Ride
from authentication.models import Profile
from django.utils import timezone
import os

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
    
