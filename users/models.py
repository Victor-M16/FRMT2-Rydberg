from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse



#user models
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                           **other_fields)
        user.set_password(password)
        user.save()
        return user
    

class NewUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('Collector', 'collector'),
        ('Revenue Creator', 'revenue creator'),
        ('Council Official', 'council official'),
        ('Admin', 'admin'),
    )

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    user_type = models.CharField(max_length=150, null=True, choices=USER_TYPE_CHOICES)
    start_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name
    
    def get_absolute_url(self):
        return reverse("frmt-newuser-detail", kwargs={"pk": self.pk})
    


#revenue models
class Revenue(models.Model):
    REVENUE_TYPE_CHOICES = [
        ('Market Fee', 'market fee'),
        ('Business Tax', 'business tax'),
        ('City Rate', 'city rate'),
        ('License Fee', 'license fee')
    ]

    revenueID=models.AutoField(primary_key=True)
    revenue_type = models.CharField(max_length=150, choices=REVENUE_TYPE_CHOICES, unique=True)
    rate = models.DecimalField(max_digits=20, decimal_places=2)
    
    def __str__(self):
        return self.revenue_type


#registered business models
class Business(models.Model):
    name = models.CharField(max_length=150)
    owner = models.CharField(max_length=150)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse("frmt-business-detail", kwargs={"pk": self.pk})



#collection instances implementation
class Collection_instance(models.Model):
    
    name=models.CharField(max_length=150, null=True)
    jurisdiction = models.CharField(max_length=150)
    collector = models.ForeignKey(NewUser, verbose_name=_("Collector"), on_delete=models.CASCADE)
    collected_revenue = models.ForeignKey(Revenue, on_delete=models.CASCADE, to_field='revenue_type')
    amount = models.DecimalField(max_digits=20, decimal_places=2, null=True)

    def __str__(self):
        return self.name 
    
    def get_absolute_url(self):
        return reverse("frmt-CI-detail", kwargs={"pk": self.pk})
    
    
@receiver(post_save, sender=Collection_instance)
def update_collector(sender, instance, **kwargs):
    # Only set the collector field if the associated NewUser has user_type 'collector'
    if instance.collector and instance.collector.user_type != 'Collector':
        instance.collector = None  # Clear the collector field if the user_type is not 'collector'
        instance.save()
      



#transaction models
class Transaction(models.Model):
    STATUSES=(('P','Pending'),
              ('C','Completed'),
              ('F','Failed') 
              )
    
    payerID = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='payer_id')
    collectorID = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='collector_id')
    revenueID=models.ForeignKey(Revenue, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    receipt_info = models.CharField(max_length=150)
    date_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=150, choices=STATUSES)

    def __str__(self):
        return self.receipt_info
    
    def get_absolute_url(self):
        return reverse("frmt-transaction-detail", kwargs={"pk": self.pk})
    


#property models
class Property(models.Model):
    LAND_USE_TYPES=(('Domestic','Domestic'),
              ('Commercial','Commercial'),
              )

    plot_number = models.CharField( max_length=50, unique=True)
    land_use = models.CharField(max_length=20, choices=LAND_USE_TYPES)
    capital_value = models.DecimalField(max_digits=30, decimal_places=2)
    name = models.CharField(max_length=150)
    rates_owed = models.DecimalField(max_digits=30, decimal_places=2, null= True)


    class Meta:
        verbose_name = _("Property")
        verbose_name_plural = _("Properties")

    def __str__(self):
        return self.plot_number

    def get_absolute_url(self):
        return reverse("frmt-property-detail", kwargs={"pk": self.pk})



