from rest_framework import serializers
from .models import DataUji
from algoritma.utils import ekstraksi_ciri
from skimage import io, img_as_ubyte,color, transform
from django.conf import settings
import os
class SerializerDataUji(serializers.ModelSerializer):
    image = serializers.ImageField()
    feature = serializers.CharField(read_only=True)
    kelas = serializers.CharField(read_only=True)
    
    class Meta:
        model = DataUji
        fields = ['id', 'image', 'feature', 'kelas']
        
    def create(self, validated_data):
        instance = super().create(validated_data)
        img = io.imread(instance.image.path, as_gray=True)
        img = img_as_ubyte(img)
        instance.filename = instance.image.path.replace(str(settings.MEDIA_ROOT), '')
        # instance.feature = ekstraksi_ciri(instance.image.path)
        instance.save()
        return instance
