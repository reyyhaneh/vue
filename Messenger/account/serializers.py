from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, Contact


class UserSerializer(serializers.ModelSerializer):
    contacts = serializers.SerializerMethodField()

    def get_contacts(self,obj):
        return ContactRetrieveSerializer(Contact.objects.filter(user=obj),many=True).data
    class Meta:
        model = User
        fields = '__all__'


class UserMainInfoSerializer(UserSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return 'http://localhost:8000' + obj.image.url
        return None

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'image','phone','bio']


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'username', 'password', 'first_name', 'last_name', 'bio', 'image']

    def create(self, validated_data):
        if User.objects.filter(phone=validated_data['phone']).exists():
            raise serializers.ValidationError('This phone number is already registered')
        elif User.objects.filter(phone=validated_data['username']).exists():
            raise serializers.ValidationError('This username is already registered')

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


class ContactRetrieveSerializer(ContactSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return UserMainInfoSerializer(obj.user).data

    class Meta:
        model = Contact
        fields = '__all__'
