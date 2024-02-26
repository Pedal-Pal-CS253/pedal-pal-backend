from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "is_subscribed",
            "ride_active",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_subscribed": {"read_only": True},
        }


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("id", "email", "first_name", "last_name", "phone", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Profile.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = Profile.objects.filter(email=email).first()
            if user:
                if user.check_password(password):
                    return user
                else:
                    raise serializers.ValidationError("Incorrect password.")
            else:
                raise serializers.ValidationError("User does not exist.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class BlankUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = []


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "phone")

    def validate(self, data):
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")

        if first_name is None and last_name is None and phone is None:
            raise serializers.ValidationError(
                "At least one field must be provided to update the profile"
            )
        return data
