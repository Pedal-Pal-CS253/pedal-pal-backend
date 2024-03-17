from authentication.models import Profile
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import (
    ProfileSerializer,
    RegisterSerializer,
    LoginSerializer,
    ChangePasswordSerializer,
)
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.decorators import renderer_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import update_session_auth_hash

from .email import send_otp_via_email


class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        send_otp_via_email(user.email)
        return Response(
            {
                "user": ProfileSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )


@api_view(("POST", "GET"))
@renderer_classes((JSONRenderer,))
@authentication_classes([])
@permission_classes([])
@csrf_exempt
def activate_account(request, id, otp):
    try:
        user = Profile.objects.get(id=id)
    except Profile.DoesNotExist:
        return Response(
            {"error": "User does not exist."}, status=status.HTTP_400_BAD_REQUEST
        )

    if user.otp == str(otp):
        user.is_active = True
        user.save()
        return Response(
            {"message": "Account activated successfully."},
            status=status.HTTP_200_OK,
        )

    return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        login(request, user)
        return Response(
            {
                "user": ProfileSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == "POST":
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get("old_password")):
                user.set_password(serializer.data.get("new_password"))
                user.save()
                update_session_auth_hash(request, user)
                return Response(
                    {"message": "Password changed successfully."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Incorrect old password."}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAuthToken(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class GetUserDetailsAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response(
            {
                "user": ProfileSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )


class SubscribeAPI(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        value = request.data["value"]
        if user.check_subscription() == value:
            msg = "User already has a subscription"
            if not value:
                msg = "User does not have a subscription"

            return Response(
                {"message": msg},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.subscribe(value)
        return Response(status=status.HTTP_200_OK)
