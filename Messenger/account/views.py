from rest_framework import generics, status, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, mixins

from chat.models import Chat
from .serializers import *

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'uid': user.id,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print(1)
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(username=username, password=password)
        if user:
            return Response(get_tokens_for_user(user))
        if User.objects.filter(username=username).exists():
            return Response({"error": "password is incorrect"}, status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        return Response({"error": "user with this username does not exist"},
                        status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)


class RegisterAPI(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):

    def filter_users(self, keyword):
        ids = [u.id for u in User.objects.all() if
               keyword in u.get_full_name() or keyword in u.username or keyword in u.phone]
        return User.objects.filter(id__in=ids)

    def get_queryset(self):
        self.serializer_class = UserSerializer
        if self.action in ['list'] and 'keyword' in self.request.query_params:
            keyword = self.request.query_params['keyword']
            self.serializer_class = UserMainInfoSerializer
            return self.filter_users(keyword)
        return User.objects.filter(id=self.request.user.id)


class ContactViewSet(viewsets.ModelViewSet):
    def check_permissions(self, request):
        if self.kwargs['user_id'] != self.request.user.id:
            self.permission_denied(request, message='Access denied!', code=401)

        mutable = None
        if hasattr(request.data, '_mutable'):
            mutable = request.data._mutable
            request.data._mutable = True
        request.data['user'] = request.user.id
        if mutable != None:
            request.data._mutable = mutable
        super().check_permissions(request)

    def get_queryset(self):
        if self.action in ['get', 'list', 'retrieve']:
            self.serializer_class = ContactRetrieveSerializer
        return Contact.objects.filter(user=self.request.user)

    serializer_class = ContactSerializer


class CheckUsernameAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({'unique': User.objects.filter(username=request.data['username']).exists() == False})


class CheckPhoneAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        return Response({'unique': User.objects.filter(phone=request.data['phone']).exists() == False})


class ChatContact(APIView):
    def get(self, request, pk):
        contact = Contact.objects.get(id=pk)
        c_user = contact.contact

        chat = None
        for c in Chat.objects.all():
            if request.user in c.users.all() and c_user in c.users.all():
                chat = c.id
        ser = UserMainInfoSerializer(c_user).data
        ser['chat'] = chat
        try:
            c = Contact.objects.filter(user=request.user, contact=c_user).first()
            ser['contact_name'] = c.contact_name
            ser['cid'] = c.id
        except:
            ser['contact_name'] = None
            ser['cid'] = None
        return Response(ser)


class AddContact(APIView):
    def post(self, request):
        contact_name = request.data['contact_name']
        username = request.data['username']
        if not User.objects.filter(username=username).exists:
            raise ValidationError({'message':'username does not exist'},code=400)
        try:
            c = Contact.objects.create(user=request.user, contact_name=contact_name,
                                   contact=User.objects.get(username=username))
        except:
            raise ValidationError({'message':'cpntact name must be unique'},code=400)

        return Response(ContactRetrieveSerializer(c).data)

