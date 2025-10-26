from django.db import models
from django.db.models.signals import post_save # helps 
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, middle_name=None, password=None, **extra_fields):
        """
        Creates and returns a regular user with the given email, first name, and password.
        """
        if not email:
            raise ValueError('The email field must be set')
        if not first_name:
            raise ValueError('The First Name field must be set')

 
        user = self.model(
            email=email,
            first_name=first_name,
            middle_name=middle_name,
            
            **extra_fields
        )
        if password:
            user.set_password(password)  # Hash the password
        else:
            user.set_unusable_password()  # Prevent login if no password is provided

        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password=None, **extra_fields):
        """
        Creates and returns a superuser with the given email, first name, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, first_name, password=password, **extra_fields)
class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.name

class User(AbstractUser):
    first_name = models.CharField(max_length=255, null=False)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True)
    email= models.EmailField( max_length=254,unique=True)
    photo = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True,blank=True, related_name='users')
    status = models.CharField(max_length=255, default='Active')
    removed = models.BooleanField(default=False)
    enabled = models.BooleanField(default=True)
    created = models.DateTimeField(default=timezone.now)
    isLoggedIn = models.IntegerField(default=0)
    USERNAME_FIELD = 'email'  # Use phone as the username
    REQUIRED_FIELDS = ['first_name',]
    objects = UserManager()

    def save(self, *args, **kwargs):
        
        if not self.password:   
            self.set_password("changeme")  # Use set_password to hash the default password
        super().save(*args, **kwargs)  

    def __str__(self):
        return f'{self.first_name}'

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
   
    class Meta:
        unique_together = ('user', 'role')   
    
    def __str__(self):
        return f'{self.user.first_name} - {self.role.name}'


class UserLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.user} - {self.action} at {self.timestamp}"
   
    
    