from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser


phone_regex = RegexValidator(regex=r'^\0?1?\d{9,20}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 20 digits allowed.")


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password, **extra_fields):
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)


class User(AbstractUser):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=13, unique=True, validators=[phone_regex])
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    image = models.ImageField(null=True,blank=True)
    bio = models.TextField(blank=True)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['username']
    objects = CustomUserManager()
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_contacts')
    contact = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_user')
    contact_name = models.CharField(max_length=255)

