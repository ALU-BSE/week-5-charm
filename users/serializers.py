from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import User, Passenger, Rider


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone_number', 'user_type']


class PassengerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Passenger
        fields = [
            'id', 'user', 'passenger_id', 'preferred_payment_method', 
            'home_address', 'profile_picture', 'preferred_language', 
            'emergency_contact', 'is_verified', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RiderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Rider
        fields = [
            'id', 'user', 'profile_picture', 'license_number', 'license_picture',
            'id_number_picture', 'verification_status', 'verification_notes',
            'is_available', 'current_latitude', 'current_longitude', 
            'average_rating', 'total_rides', 'total_earnings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'average_rating', 'total_rides', 'total_earnings', 'created_at', 'updated_at']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords dont match'})
        validate_password(data['password]'])
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
