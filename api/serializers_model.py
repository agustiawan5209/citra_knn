from rest_framework import serializers
from algoritma.models import DataLatih

class DataLatihSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataLatih
        fields = ['id', 'nama', 'kelas', 'image']
