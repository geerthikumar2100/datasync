from django.db import models
import uuid
import secrets
from django.core.validators import EmailValidator, URLValidator
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from datasync.settings import AUTH_USER_MODEL
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import EmailValidator
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        
        extra_fields.pop("username", None)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None  # Remove username field
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="created_users")
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_users")

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email



class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_name = models.CharField(unique=True, max_length=255)
    app_secret_token = models.CharField(max_length=255, unique=True, editable=False)
    website = models.URLField(blank=True, null=True, validators=[URLValidator()])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_accounts")
    updated_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="updated_accounts")

    def save(self, *args, **kwargs):
        """Automatically generate `app_secret_token` only for new accounts."""
        if not self.app_secret_token:
            self.app_secret_token = secrets.token_urlsafe(32)  # Generate a secure random token
        super().save(*args, **kwargs)

    def __str__(self):
        return self.account_name

@receiver(pre_delete, sender=Account)
def delete_related_objects(sender, instance, **kwargs):
    instance.destinations.all().delete()
    instance.members.all().delete()
    instance.logs.all().delete()

class Role(models.Model):
    ADMIN = "Admin"
    USER = "User"
    ROLE_CHOICES = [(ADMIN, "Admin"), (USER, "User")]

    id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, choices=ROLE_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role_name

class AccountMember(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="account_memberships")
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_members")
    updated_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="updated_members")

    class Meta:
        unique_together = ("account", "user")

    def __str__(self):
        return f"{self.user.email} - {self.account.account_name} - {self.role.role_name}"

class Destination(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="destinations")
    url = models.URLField()
    http_method = models.CharField(max_length=10, choices=[("GET", "GET"), ("POST", "POST"), ("PUT", "PUT")])
    headers = models.JSONField(blank=True, null=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_destinations")
    updated_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="updated_destinations")

    def __str__(self):
        return f"{self.account.account_name} - {self.url}"

class Log(models.Model):
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="logs")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="logs")
    received_timestamp = models.DateTimeField()
    processed_timestamp = models.DateTimeField()
    received_data = models.JSONField()
    status = models.CharField(max_length=10, choices=[("success", "Success"), ("failed", "Failed")])

    def __str__(self):
        return f"Log {self.event_id} - {self.status}"
