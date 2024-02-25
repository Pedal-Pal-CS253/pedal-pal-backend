from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import ProfileSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.utils.translation import gettext_lazy as _
from rest_framework import status


class RegisterAPI(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": ProfileSerializer(
                    user, context=self.get_serializer_context()
                ).data,
            }
        )


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


class PasswordResetAPI(PasswordResetView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PasswordResetConfirmAPI(PasswordResetConfirmView):
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
