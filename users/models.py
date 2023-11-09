from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, first_name, password, **other_fields)

    def create_user(self, email, user_name, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user





class NewUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('Collector', 'Collector'),
        ('Council Official', 'Council Official'),
        ('Business Owner', 'Business Owner'),
    )

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    user_type = models.CharField(max_length=150, null=True)
    start_date = models.DateTimeField(default=timezone.now)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','user_type']

    def __str__(self):
        return self.user_name
    

class Council(models.Model):
    """
    Represents a council with email, name, and a unique identifier.

    Attributes:
        email (str): The email address of the council.
        name (str): The name of the council.
        councilID (int): The unique identifier for the council.

    Meta:
        verbose_name (str): A human-readable name for the model.
        verbose_name_plural (str): A human-readable plural name for the model.

    Methods:
        __str__(): Returns a string representation of the council, which is its name.
    """

    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=150, unique=True)
    councilID=models.AutoField(primary_key=True)
        
    class Meta:
        verbose_name = _("Council")
        verbose_name_plural = _("Councils")

    def __str__(self):
        return self.name


class Location(models.Model):
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Service(models.Model):
    service_TYPE_CHOICES = (
        ('Market Fee', 'Market Fee'),
        ('Business Tax', 'Business Tax'),
        ('Rent', 'Rent'),
    )

    serviceID=models.AutoField(primary_key=True)
    council = models.ForeignKey(Council, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    type = models.CharField(max_length=150, null=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)
    
    def __str__(self):
        return self.name
 

class Notification(models.Model):
    notificationID=models.BigAutoField(primary_key=True)
    userID = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=150)
    date_time = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message
    

class Transaction(models.Model):
    STATUSES=['Pending', 'Completed', 'Failed']
    
    transationID=models.BigAutoField(primary_key=True)
    payerID = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='payer_id')
    collectorID = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='collector_id')
    serviceID=models.ForeignKey(Service, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    councilID = models.ForeignKey(Council, on_delete=models.CASCADE)
    receipt_info = models.CharField(max_length=150)
    date_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=150)

    def __str__(self):
        return self.receipt_info
    

class Issue(models.Model):
    STATUSES=['In-progress', 'Open', 'Closed']
    
    issueID=models.BigAutoField(primary_key=True)
    userID = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    details = models.CharField(max_length=150)
    resolution_details = models.CharField(max_length=150)
    date_time = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=150)

    def __str__(self):
        return self.details
   
    
class Business(models.Model):
    businessID=models.BigAutoField(primary_key=True)
    OwnerID = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    tax_details = models.CharField(max_length=150)
    councilID = models.ForeignKey(Council, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name