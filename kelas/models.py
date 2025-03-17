from django.db import models

# Create your models here.

# Model Untuk Nama Kelas
class Kelas(models.Model):
    nama = models.CharField(max_length=50 ,unique=True)
    informasi = models.TextField()
    
    def save(self, *args, **kwargs):
        self.nama = str.lower(self.nama) 
        super().save(*args, **kwargs)
        
    def __str__(self):
        return "{}".format(self.nama)
    