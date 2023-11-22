from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .models import NewUser

#new models
class Location(models.Model):
    name = models.CharField('Location Name', max_length=120)
    
    def __str__(self):
        return self.name
    
class CollectionType(models.Model):
    name = models.CharField('Collection Name', max_length=120)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    amount = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse("frmt-CT-detail", kwargs={"pk": self.pk})
    
    
class CollectionInstance(models.Model):
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    collector = models.ForeignKey(NewUser, verbose_name=_("Collector"), on_delete=models.CASCADE)
    collection_type = models.ForeignKey(CollectionType, on_delete=models.CASCADE)
    amount = models.CharField(max_length=60)

    def __str__(self):
        return self.location.name +'/'+ self.collector.user_name +'/'+ self.collection_type.name +'/'+ self.amount
    
    # def get_absolute_url(self):
    #     return reverse("frmt-CIns-detail", kwargs={"pk": self.pk})
    