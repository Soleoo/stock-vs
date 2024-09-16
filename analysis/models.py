from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, full_name, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, full_name, password, **extra_fields)

class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('Visitor', 'Visitor'),
        ('Staff', 'Staff'),
        ('Admin', 'Admin'),
    )
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    access_level = models.IntegerField(default=1)
    last_recognition_time = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    face_image = models.ImageField(upload_to='face_images/', null=True, blank=True)
    
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)  
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)  

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == 'Admin':
            self.is_staff = True
            self.is_superuser = True
        super(User, self).save(*args, **kwargs)

    def clean(self):
        super().clean()
        if self.role == 'Staff' and not self.face_image:
            raise ValidationError(_('Face image is required for staff members.'))
        if self.role == 'Admin' and not self.face_image:
            raise ValidationError(_('Face image is required for admin members.'))

    def has_module_perms(self, app_label):
        if self.role == 'Admin':
            return True
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        if self.role == 'Admin':
            return True
        return self.is_superuser