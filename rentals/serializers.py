from django.forms import ValidationError
from rest_framework import serializers
from .models import User, Book, Rental
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']

    def validate(self, data):
        try:
            validate_password(password=data['password'], user=User())
        except ValidationError as e:
            raise serializers.ValidationError({'password': str(e)})

        return data

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class BookSerializer(serializers.Serializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'page_count']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'user', 'book', 'start_date', 'end_date', 'extended']
        read_only_fields = ['start_date']

