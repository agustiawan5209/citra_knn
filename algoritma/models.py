from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .utils import ekstraksi_ciri
from skimage import io, img_as_ubyte,color, transform
from skimage.transform import rescale, resize, downscale_local_mean
from django.conf import settings
from kelas.models import Kelas
import os
import uuid
from PIL import Image


# Create your models here.
def unique_filename(instance, filename):
    ext = os.path.splitext(filename)[1]
    new_filename = filename
    # new_filename = uuid.uuid4().hex[:10] + ext
    return os.path.join('datalatih/', new_filename)

class DataLatih(models.Model):
    nama = models.CharField(max_length=30)
    image = models.ImageField(upload_to=unique_filename)
    feature = models.TextField(blank=True)
    kelas = models.ForeignKey(Kelas, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Check if an object with the same image and kelas values already exists
        existing_object = DataLatih.objects.filter(pk=self.pk).first()
        if existing_object:
            # If an existing object is found, update it instead of creating a new one
            self.feature = ekstraksi_ciri(self.image.path)
            existing_object.feature = self.feature
            existing_object.save()
            return

        # If no existing object is found, create a new one
        super().save(*args, **kwargs)  # Save the image first
        img = io.imread(self.image.path, as_gray=True)
        img = img_as_ubyte(img)
        self.feature = ekstraksi_ciri(self.image.path)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return "{}".format(self.nama)
    

@receiver(pre_delete, sender=DataLatih)
def image_delete(sender, instance, **kwargs):
    """Deletes the associated image file when the Image model instance is deleted."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
            
