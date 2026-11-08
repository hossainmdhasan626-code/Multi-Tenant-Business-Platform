# ---Django---
from django.contrib.auth.password_validation import validate_password

# ---Drf---
from rest_framework import serializers

# ---Model---
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "created_date",
            "updated_date",
        ]
        read_only_fields = ["id", "created_date", "updated_date"]

    # # Password validate
    # def validate_password(self, value):
    #     validate_password(value)
    #     return value

    # Password hash
    def create(self, validated_data):

        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
