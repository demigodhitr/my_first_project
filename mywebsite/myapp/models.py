from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group, Permission, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
import random
import string


#this is for managing my users.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


    is_superuser = models.BooleanField(default=False)  # Manually defining is_superuser because i am using my own custom user model instead of Django built-in user model.

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username', 'last_name']

    def __str__(self):
        return self.username
    
@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = f'Welcome to BitProfitOnline, {instance.first_name}!'
        message = render_to_string('welcome_email.html', {'user': instance})
        from_email = 'alerts@bitprofitonline.com'
        recipient_list = [instance.email]
        send_mail(
            subject, 
            message, 
            from_email, 
            recipient_list,
            html_message=message,
        )
    
#account info model

class AccountInfo(models.Model):
    verification_choices = [
        ('Under review', 'Under Review'),
        ('Awaiting', 'Awaiting'),
        ('Failed', 'Failed'),
        ('Verified', 'Verified'),]
    
    trade_choices = [
        ('Active', 'Active'), 
        ('Inactive', 'Inactive'),
        ('Suspended', 'Suspended'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Paused', 'Paused'),
        ('No Trade', 'No Trade'),]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    nationality = models.CharField(max_length=50, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    Deposit = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null=True, blank=True)
    Bonus = models.DecimalField(default=15.00, max_digits=10, decimal_places=2, null=True, blank=True)
    Profits = models.DecimalField(default=0.00, max_digits=10, decimal_places=2, null=True, blank=True)
    Withdrawal_limit = models.DecimalField(default=7000.00, max_digits=10, decimal_places=2, null=True, blank=True)
    TradeIsActive = models.BooleanField(default=False)
    CanWithraw = models.BooleanField(default=False)
    TradeStatus = models.CharField(max_length=30, default='No Trade', choices=trade_choices)
    verificationStatus = models.CharField(max_length=50, default='Awaiting', null=True, blank=True,choices=verification_choices)

    @property
    def total_balance(self):
        return self.Deposit + self.Bonus + self.Profits
    
#notifications model

class newNotifications(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default='Welcome Investor')
    message = models.TextField(default='Thank you for joining us. Should you have any questions or concerns, kindly open a chat and an admin will be assigned to you.')
    created_at = models.DateTimeField(auto_now_add=True)

#terms and conditions model

class TermsAndCondition(models.Model):
    Title = models.CharField(max_length=100)
    message = models.TextField(max_length=5000)
    message2 = models.TextField(max_length=5000, null=True, blank=True)

# Withdrawal request model.
class WithdrawalRequest(models.Model):
    options = [
        ('Checking', 'Checking'),
        ('Paid', 'Paid'),
        ('Under review', 'Under review'),
        ('Failed', 'Failed'),
        ('Approved, Pending', 'Approved, Pending'),]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    network = models.CharField(max_length=100, default='no data')
    address = models.CharField(max_length=255, default='no data')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=30, default='Checking', choices=options) 
    created_at = models.DateTimeField(auto_now_add=True)
    RequestID = models.IntegerField(default=00000000, blank=True, null=True)

#wallet address model

class WalletAddress(models.Model):
    bitcoin = models.CharField(max_length=150)

    ethereum = models.CharField(max_length=150)

    tether_USDT = models.CharField(max_length=150)

    ERC20_address = models.CharField(max_length=150)

# Deposit model

class Deposit(models.Model):
    options = [
        ('No deposit', 'No Deposit'),
        ('Invalid', 'Invalid'),
        ('Failed', 'Failed'),
        ('Under review', 'Under review'),
        ('Confirmed', 'Confirmed'),
        ('Credited', 'Credited'),]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    DepositAmount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00, null=True, blank=True)
    Network = models.CharField(max_length=100, null=True, blank=True)
    Proof = models.ImageField(upload_to='payments/', null=True, blank=True)
    status = models.CharField(max_length=50, default='', choices=options)
    requestID = models.CharField(default='', max_length=8, null=True, blank=True)
    Confirmed = models.BooleanField(default=False)
    not_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.requestID:
            self.requestID = ''.join(random.choices(string.digits, k=8))
        super().save(*args, **kwargs)




class IDME(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, null=True, blank=True)
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True )
    DOB = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    id_front = models.ImageField(upload_to='id_cards/', null=True, blank=True)
    id_back = models.ImageField(upload_to='id_cards/', null=True, blank=True)
    phone = models.CharField(max_length=15, default='')




class ClientMessages(models.Model):
    fullName = models.CharField(max_length=250, null=True, blank=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    message = models.TextField(null=True, blank=True)


