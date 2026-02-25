from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

# Create your models here.

class CommonBaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        abstract = True

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin): 
    GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    ]

    RELATIONSHIP = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('in_a_relationship', 'In a Relationship'),
    ]

    
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=False, blank=False)
    relationship = models.CharField(max_length=100, choices=RELATIONSHIP, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email
    
   

class Profile(CommonBaseModel):
    GENDER = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    ]

    RELATIONSHIP = [
    ('single', 'Single'),
    ('married', 'Married'),
    ('in_a_relationship', 'In a Relationship'),
    ]

    STATUS = [
    ('online', 'Online'),
    ('offline', 'Offline'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True) 
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    profile_picture = models.ImageField(upload_to='media/profile_pictures', null=True, blank=True, default="default.png")    
    cover_photo = models.ImageField(upload_to='media/cover_photos', null=True, blank=True, default="cover.png")
    bio = models.TextField(null=True, blank=True)
    major = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS, null=True, blank=True, default="single")
    
    def save(self, *args, **kwargs):
        if not self.profile_picture:
            self.profile_picture = 'default.png'
        if not self.cover_photo:
            self.cover_photo = 'cover.png'
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.firstname}"
