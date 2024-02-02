from rest_framework import generics, status, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, mixins

from account.models import Contact
from account.serializers import ContactSerializer, ContactRetrieveSerializer
from .models import User, Chat, Message
from .serializers import *

from django.db.models import Q


class ChatViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    def get_queryset(self):
        return self.request.user.chat_set.all()

    serializer_class = ChatSerializer

    def add_curr_user(self):
        data = self.request.data
        if not 'users' in data:
            raise ValidationError({'message': 'users must be specified'}, code=400)
        mutable = None
        if hasattr(data, '_mutable'):
            mutable = data._mutable
            data._mutable = True

        data['users'].append(self.request.user.id)
        if mutable != None:
            data._mutable = mutable

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True).data
        for data in serializer:
            unread_count = Chat.objects.get(id=data['id']).message_set.exclude(sender=request.user).filter(
                seen=False).count()
            for uid in data['users']:
                if uid != request.user.id:
                    contact_user = UserMainInfoSerializer(User.objects.get(id=uid)).data
                    try:
                        contact_name = Contact.objects.get(contact__id=uid, user=request.user).contact_name
                    except:
                        contact_name = User.objects.get(id=uid).get_full_name()
                    data['name'] = contact_name
                    data['contact_user'] = contact_user
                    data['unread_count'] = unread_count

        return Response(serializer)

    def create(self, request, *args, **kwargs):
        self.add_curr_user()
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = ChatRetrieveSerializer
        instance = self.get_object()
        contact_name = None
        for u in instance.users.all():
            if u != request.user:
                contact_user = UserMainInfoSerializer(u).data
                try:
                    contact_name = Contact.objects.get(contact=u, user=request.user).contact_name
                except:
                    contact_name = u.get_full_name()
        serializer = self.get_serializer(instance).data
        serializer['name'] = contact_name
        serializer['contact_user'] = contact_user

        for msg in serializer['messages']:
            msg['sent_by_me'] = False
            if msg['sender'] == request.user.id:
                msg['sent_by_me'] = True

        for msg in instance.message_set.exclude(sender=request.user):
            msg.seen = True
            msg.save()
        return Response(serializer)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def check_permissions(self, request):
        if not Chat.objects.get(id=self.kwargs['chat_id']) in self.request.user.chat_set.all():
            self.permission_denied(request, message='Access denied!', code=401)
        super().check_permissions(request)

    def get_queryset(self):
        if self.action in ['update', 'patch', 'delete']:
            return Message.objects.filter(sender=self.request.user, chat=self.kwargs['chat_id'])
        return Message.objects.filter(chat=self.kwargs['chat_id'])

    def create(self, request, *args, **kwargs):
        mutable = None
        if hasattr(request.data, '_mutable'):
            mutable = request.data._mutable
            request.data._mutable = True
        request.data['sender'] = request.user.id
        request.data['chat'] = self.kwargs['chat_id']
        if mutable != None:
            request.data._mutable = mutable
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MessageUpdateSerializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(MessageSerializer(instance).data)


class ChatContact(APIView):
    def get(self, request, pk):
        chat = Chat.objects.get(id=pk)
        c_user = chat.users.exclude(id=request.user.id).first()
        ser = UserMainInfoSerializer(c_user).data
        ser['chat'] = chat.id
        try:
            c=Contact.objects.filter(user=request.user, contact=c_user).first()
            ser['contact_name'] = c.contact_name
            ser['cid'] = c.id
        except:
            ser['contact_name'] = None
            ser['cid'] = None
        return Response(ser)
