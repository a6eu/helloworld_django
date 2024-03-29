from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.utils import timezone
import random
import string


class UserProfileManager(BaseUserManager):

    def create_user(self, first_name, last_name, phone_number, email, password=None):
        if not email:
            raise ValueError('Пользователи должны иметь адрес электронной почты или номер телефона')
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, phone_number=phone_number, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, phone_number, email, password):
        user = self.create_user(first_name, last_name, phone_number, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Role(models.Model):
    name = models.CharField(max_length=255, default="User")

    def __str__(self):
        return self.name


class UserProfile(AbstractBaseUser, PermissionsMixin):

    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    CHOICES = [
        (MALE, "male"),
        (FEMALE, "female"),
        (OTHER, "other")
    ]

    phone_number_regex = RegexValidator(
        regex=r'\d{10}$', message="Numbers without +7/8"
    )

    password_validator = RegexValidator(
        regex=r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$',
        message="Пароль должен быть длиной от 8 до 20 символов, начинаться с буквы и содержать как минимум одну цифру."
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(validators=[phone_number_regex], unique=True, max_length=10, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=255, unique=False)
    gender = models.CharField(max_length=255, blank=True, null=True, choices=CHOICES)
    birth_day = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to="01it.group/users/", null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    password = models.CharField(validators=[password_validator], max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_profiles',
        blank=True,
        help_text='The groups this user belongs to',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_profiles',
        blank=True,
        help_text='Specific permissions for this user',
        verbose_name='user permissions',
    )
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone_number']

    def __str__(self):
        return self.email


class PasswordResetToken(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=7, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reset_code:
            self.reset_code = self.generate_reset_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_reset_code(length=7):
        characters = string.ascii_letters + string.digits
        while True:
            code = ''.join(random.choices(characters, k=length))
            if not PasswordResetToken.objects.filter(reset_code=code).exists():
                return code

    def is_valid(self):
        return (timezone.now() - self.created_at).total_seconds() < 3600

    def __str__(self):
        return f"PasswordResetToken for {self.user}"
