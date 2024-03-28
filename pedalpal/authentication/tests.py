from rest_framework.test import APITestCase
from .models import Profile


class AuthenticationTestCase(APITestCase):
    def test_registration(self):
        data = {
            "email": "test@test.com",
            "password": "testpassword",
            "first_name": "test",
            "last_name": "user",
            "phone": "1234567890",
        }

        # check if able to register
        response = self.client.post("/auth/register/", data)
        self.assertEqual(response.status_code, 200)

        # check if token generated successfully
        response = self.client.post("/auth/get_auth_token/", data)
        self.assertEqual(response.status_code, 200)

        # register again using same credentials, should give error
        response = self.client.post("/auth/register/", data)
        self.assertEqual(response.status_code, 400)

    def test_login(self):
        data = {
            "email": "test@test.com",
            "password": "testpassword",
            "first_name": "test",
            "last_name": "user",
            "phone": "1234567890",
        }

        self.client.post("/auth/register/", data)
        response = self.client.post("/auth/login/", data)

        self.assertEqual(response.status_code, 200)

        # try logging in with wrong password
        data["password"] = "wrongpassword"
        response = self.client.post("/auth/login/", data)

        self.assertEqual(response.status_code, 400)

    def test_otp_verification(self):
        data = {
            "email": "test@test.com",
            "password": "testpassword",
            "first_name": "test",
            "last_name": "user",
            "phone": "1234567890",
        }

        self.client.post("/auth/register/", data)

        response = self.client.post("/auth/login/", data)
        self.assertEqual(response.status_code, 200)

        otp = Profile.objects.get(email="test@test.com").otp

        response = self.client.get(f"/auth/verify/1/{otp}/")
        self.assertEqual(response.status_code, 200)

        # try verifying with wrong otp
        response = self.client.get(f"/auth/verify/1/{int(otp)+1}/")
        self.assertEqual(response.status_code, 400)
