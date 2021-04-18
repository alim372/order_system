from django.db import models
from .managers import  SoftDeleteManager
from authentication.models import User

# -----------------(choices)------------------
class StatusChoices(models.TextChoices):
    ACTIVE = 'active'
    INACTIVE = 'inactive'
    DELETED = 'deleted'

""""""""""""""""""""""""""""""
# products model.
""""""""""""""""""""""""""""""
class Product(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    name = models.CharField(max_length=256, blank=False, null=False)
    description = models.CharField(max_length=1024, blank=True, null=True)
    price_eur = models.FloatField(blank=False, null=False)
    
    # General
    status = models.CharField(
        max_length=16, choices=StatusChoices.choices,  default=StatusChoices.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    objects = SoftDeleteManager()

    class Meta:
        db_table = "products"

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)

    def clean(self):
        super().clean()

    def str(self):
        return str(self.id)

    @staticmethod
    def protected():
        return ['updated_at', 'created_at', 'status']

""""""""""""""""""""""""""""""
# user products model.
""""""""""""""""""""""""""""""
class UserProduct(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,  null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,  null=True, blank=True)
    count = models.IntegerField(default=1)
    # General
    status = models.CharField(
        max_length=16, choices=StatusChoices.choices,  default=StatusChoices.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)
    objects = SoftDeleteManager()
    class Meta:
        db_table = "user_products"

    def save(self, **kwargs):
        self.full_clean()
        super().save(**kwargs)

    def clean(self):
        super().clean()

    def str(self):
        return str(self.id)

    @staticmethod
    def protected():
        return ['updated_at', 'created_at', 'status']


