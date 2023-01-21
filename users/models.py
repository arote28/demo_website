from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from .managers import CustomUserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    SUPERUSER = 0
    ADMIN = 1
    SELLER = 2
    BUYER = 3

    ROLE_CHOICES = (
        (SUPERUSER, 'superuser'),
        (ADMIN,'Admin'),
        (SELLER,'Seller'),
        (BUYER,'Buyer')
    )

    # username = models.CharField(max_length=30, blank=False,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    mobile_number = models.CharField(max_length=12)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=False, null=False, default=3)
    # date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)

    # EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



    # def clean_username(self):
    #     username = self.cleaned_data.get("username")
    #     if User.objects.filter(username__iexact=username).exists():
    #         self.add_error("username", "A user with this username already exists.")
    #     return username
    #
    # def clean(self):
    #     super().clean()
    #     self.email = self.__class__.objects.normalize_email(self.email)
    #     self.username = self.username.lower()



    def __str__(self):
        return self.email
