from django.db import models
from .managers import CustomUserManager, SoftDeleteManager
from django.contrib.auth.models import AbstractUser

# -----------------(choices)------------------
class StatusChoices(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

class UserTypeChoices(models.TextChoices):
    USER = 'user'
    ADMINISTRATOR = 'administrator'

# custom user model.
class User(AbstractUser):
    id = models.AutoField(primary_key=True, serialize=False)
    username = models.CharField(
        max_length=256, blank=False, null=False, unique=True)
    email = models.EmailField(
        max_length=256, blank=False, null=False, unique=True)
    last_name = models.CharField(
        max_length=256, blank=False, null=False)
    first_name = models.CharField(
        max_length=256, blank=False, null=False)
    type = models.CharField(
        max_length=32, choices=UserTypeChoices.choices,  default=UserTypeChoices.USER)
    items = CustomUserManager()
    # General
    status = models.CharField(
        max_length=16, choices=StatusChoices.choices,  default=StatusChoices.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = "users"

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)

    def clean(self):
        super().clean()

    def str(self):
        return str(self.id)

    @staticmethod
    def protected():
        return ['updated_at', 'created_at','password' , 'status', 'type']
