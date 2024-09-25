from django.db import models
from django.contrib.auth.models import *
# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

class CustomUser(TimeStampedModel, AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
    
class ImageUpload(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='uploads/',null=True, blank=True)
    result_image = models.ImageField(upload_to='results/',null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s image uploaded at {self.uploaded_at}"