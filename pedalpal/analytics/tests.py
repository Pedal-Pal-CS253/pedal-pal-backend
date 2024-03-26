from rest_framework.test import APITestCase
from authentication.models import ProfileManager, Profile
from booking.models import Ride, Booking, Cycle, Hub, Lock
from booking.serializers import RideSerializer, BookingSerializer


class AnalyticsTestCase(APITestCase):
    def set_up(self):
        profile_manager = ProfileManager()
        profile_manager.model = Profile
        self.user = profile_manager.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="1234567890",
            password="test",
        )

        self.user.is_active = True
        self.user.save()

        data = {
            "email": "test@test.com",
            "password": "test",
        }

        response = self.client.post("/auth/get_auth_token/", data, format="json")
        self.token = response.data["token"]

        self.hub1 = Hub.objects.create(
            hub_name="Test Hub 1",
            max_capacity=10,
            latitude=0,
            longitude=0,
        )

        self.cycle1 = Cycle.objects.create(
            user=None,
            hub=self.hub1,
            active=False,
            booked=False,
        )

        self.lock1 = Lock.objects.create(
            hub=self.hub1,
            cycle=self.cycle1,
        )

        self.ride1 = Ride.objects.create(
            user=self.user,
            cycle=self.cycle1,
            start_time="2021-09-01T00:00:00Z",
            end_time="2021-09-01T00:10:00Z",
            cost=10,
            start_hub=self.hub1,
            end_hub=self.hub1,
        )

        self.ride2 = Ride.objects.create(
            user=self.user,
            cycle=self.cycle1,
            start_time="2021-09-02T00:00:00Z",
            end_time="2021-09-02T00:10:00Z",
            cost=10,
            start_hub=self.hub1,
            end_hub=self.hub1,
        )

        self.booking1 = Booking.objects.create(
            user=self.user,
            cycle=self.cycle1,
            hub=self.hub1,
            book_time="2021-09-01T00:00:00Z",
            start_time="2021-09-01T00:00:00Z",
            end_time="2021-09-01T00:10:00Z",
            cancelled=False,
            cost=10,
        )

        self.booking2 = Booking.objects.create(
            user=self.user,
            cycle=self.cycle1,
            hub=self.hub1,
            book_time="2021-09-02T00:00:00Z",
            start_time="2021-09-02T00:00:00Z",
            cancelled=False,
            cost=10,
        )

    def test_history(self):
        self.set_up()
        response = self.client.post(
            "/analytics/history/", HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(response.status_code, 200)

        rides = Ride.objects.filter(user=self.user)
        serializer = RideSerializer(rides, many=True)
        self.assertEqual(response.json(), serializer.data)

    def test_booking(self):
        self.set_up()
        response = self.client.get(
            "/analytics/booking_history/", HTTP_AUTHORIZATION=f"Token {self.token}"
        )

        self.assertEqual(response.status_code, 200)

        bookings = Booking.objects.filter(user=self.user)
        serializer = BookingSerializer(bookings, many=True)
        self.assertEqual(response.json(), serializer.data)
