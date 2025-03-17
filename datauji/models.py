from django.db import models
from kelas.models import Kelas
from django.contrib.auth.models import User
import uuid
import os
from django.dispatch import receiver
from django.db.models.signals import pre_delete

# Create your models here.
def unique_filename(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid.uuid4().hex[:10] + ext
    return os.path.join('datauji/', new_filename)

class DataUji(models.Model):
    filename = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to=unique_filename)
    feature = models.CharField(max_length=30, null=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return "{}".format(self.filename)
    

@receiver(pre_delete, sender=DataUji)
def image_delete(sender, instance, **kwargs):
    """Deletes the associated image file when the Image model instance is deleted."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    
    
