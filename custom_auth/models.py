from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator


class UserProfileManager(BaseUserManager):

    def create_user(self, first_name, last_name, phone_number, email, password=None):
        if not email:
            raise ValueError('Users must have an email or phone number')
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
        message="Password must be 8 to 20 characters long, start with a letter, and contain at least one digit."
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(validators=[phone_number_regex], unique=True, max_length=10)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=False)
    gender = models.CharField(max_length=255, blank=True, null=True, choices=CHOICES)
    birth_day = models.DateField(blank=True, null=True)
    city = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=255, null=True)
    avatar = models.ImageField(upload_to="01it.group/users/", null=True)
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
