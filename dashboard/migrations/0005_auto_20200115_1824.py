# Generated by Django 3.0.2 on 2020-01-15 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_service_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='attachment',
            field=models.ImageField(default='team-1.jpg', upload_to='dashboard'),
        ),
    ]
