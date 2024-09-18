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
    user_id = models.IntegerField(default=0)
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

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))
    stock = models.PositiveIntegerField(verbose_name=_("Stock"), null=True, blank=True)
    image = models.ImageField(upload_to='./media/product_images/', verbose_name=_("Product Image"), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return self.name

    def item_count(self):
        return self.items.count()
    
class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items', verbose_name=_("Product"))
    serial_number = models.CharField(max_length=255, unique=True, verbose_name=_("Serial Number"))
    qr_code = models.ImageField(upload_to='./media/qr_codes/', verbose_name=_("QR Code"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.product.name} - {self.serial_number}"