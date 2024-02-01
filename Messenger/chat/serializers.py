from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import User
from account.serializers import UserMainInfoSerializer
from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

    def validate(self, attrs):
        attrs['users'] = list(set(attrs['users']))
        if len(attrs['users']) != 2:
            raise ValidationError({'message': '2 users must be specified for the chat'}, code=400)


        return super().validate(attrs)

    def create(self, validated_data):
        users = validated_data['users']
        chats_0 = users[0].chat_set.all()
        chats_1 = users[1].chat_set.all()
        if chats_0.intersection(chats_1).count():
            raise ValidationError({'message': 'Private chat already exists'}, code=400)

        return super().create(validated_data)

class ChatRetrieveSerializer(ChatSerializer):
    messages = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_messages(self,obj):
        return MessageSerializer(obj.message_set.all(),many=True).data
    def get_users(self,obj):
        return UserMainInfoSerializer(obj.users.all(),many=True).data
    class Meta:
        model = Chat
        fields = '__all__'




class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MessageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content']
