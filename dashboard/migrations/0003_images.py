# Generated by Django 2.2 on 2020-01-15 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_delete_service_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urlhash', models.CharField(blank=True, max_length=6, null=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='dashboard')),
            ],
            options={
                'verbose_name_plural': 'Images',
            },
        ),
    ]