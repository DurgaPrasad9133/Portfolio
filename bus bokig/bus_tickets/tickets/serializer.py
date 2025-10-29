from django.contrib.auth.hashers import make_password

from . models import *

from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])  # hash the password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password)
            validated_data.pop('password')
        return super().update(instance, validated_data)

class BusesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Buses
        fields='__all__'
class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Bookings
        fields='__all__'
