from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Contact



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'username', 'first_name', 'last_name']


class UserMainInfoSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'username', 'password', 'confirm_password']

    def create(self, validated_data):
        if User.objects.filter(phone=validated_data['phone']).exists():
            raise serializers.ValidationError('This phone number is already registered')
        elif User.objects.filter(phone=validated_data['username']).exists():
            raise serializers.ValidationError('This username is already registered')

        if validated_data['password'] != validated_data.pop('confirm_password'):
            raise serializers.ValidationError('Password and confirm password are not equal')
        user = User.objects.create_user(**validated_data)
        return user

class ContactSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Contact
        fields = '__all__'

    def validate(self, attrs):
        if not 'user' in attrs:
            raise ValidationError({'message': 'user must be specified'}, code=400)
        contact, user = attrs['contact'], attrs['user']
        if contact == user:
            raise ValidationError({'message': 'you can not add yourself to you contacts'}, code=400)
        return super().validate(attrs)

    def create(self, validated_data):
        if Contact.objects.filter(user=validated_data['user'], contact_name=validated_data['contact_name']).exists():
            raise ValidationError({'message': 'contact name already exists'}, code=400)
        if Contact.objects.filter(user=validated_data['user'], contact=validated_data['contact']).exists():
            raise ValidationError({'message': 'contact already exists'}, code=400)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if Contact.objects.filter(user=validated_data['user'], contact_name=validated_data['contact_name']).exclude(
                id=instance.id).exists():
            raise ValidationError({'message': 'contact name already exists'}, code=400)
        validated_data.pop('contact')
        return super().update(instance, validated_data)
