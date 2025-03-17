# Generated by Django 4.2.13 on 2025-03-16 09:33

import datauji.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kelas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataUji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, max_length=200)),
                ('image', models.ImageField(upload_to=datauji.models.unique_filename)),
                ('feature', models.CharField(max_length=30, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('kelas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='kelas.kelas')),
            ],
        ),
    ]
