from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

    
GENDER = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("Indefined", "Indefined"),
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("bank_card", "1234123412341234")
        extra_fields.setdefault("gender", "Indefined")
        extra_fields.setdefault("contact", "+996312312312")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    bank_card = models.CharField(max_length=16, blank=True, null=True)
    contact = models.CharField(max_length=13)
    gender = models.CharField(max_length=10, choices=GENDER)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=40, blank=True)
    confirm_code = models.CharField(max_length=6, blank=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username

    def create_activation_code(self):
        import uuid
        code = str(uuid.uuid4())
        self.activation_code = code
   
    def create_confirm_code(self):
        import random
        code = str(random.randint(000000, 999999))
        self.confirm_code = code
        
    def __str__(self):
        return str(self.username)