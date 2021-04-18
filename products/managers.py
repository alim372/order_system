
from django.db import models
class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def _base_queryset(self):
        return super().get_queryset().exclude(status='deleted')

    def get_queryset(self):
        return self._base_queryset()