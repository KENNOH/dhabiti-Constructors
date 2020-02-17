from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, verbose_name='Phone Number', unique=True, blank=True, null=True)
    display_pic = models.ImageField(upload_to='accounts/', default="accounts/empty-profile.jpg", blank=True)
    # specialization = models.CharField(max_length=255, verbose_name='Select your skillset here:', blank=True, null=True)
    # bio = models.CharField(max_length=255, verbose_name='A little info about yourself', blank=True, null=True)


class specialization(models.Model):
    name = models.CharField(
        max_length=255, verbose_name='Skillset', blank=True, null=True)

    def __str__(self):
        return self.name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
