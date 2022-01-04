from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
# Create your models here.
# class Account(models.Model):
#     email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
#     username                = models.CharField(max_length=30, unique=True)
#     first_name              = models.CharField(max_length=50, blank=True, null=True)
#     # last_name               = models.CharField(max_length=50, blank=True, null=True)
#     github                  = models.CharField(max_length=100, blank=True, null=True) 
#     profile_pic             = models.TextField(blank=True, null=True)
#     bio                     = models.TextField(blank=True, null=True)
#     date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
#     last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
#     # is_admin                = models.BooleanField(default=False)
    
#     # is_active               = models.BooleanField(default=True)
#     # is_staff                = models.BooleanField(default=False)
#     # is_superuser            = models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.username


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password, profile_pic, bio, first_name, last_name, github):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email        = self.normalize_email(email),
            username     = username,
            profile_pic  = profile_pic,
            first_name   = first_name,
            last_name    = last_name,
            github       = github,
            bio          = bio
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, profile_pic='', bio='',  first_name='', last_name='', github=''):
        user = self.create_user(
            email        = self.normalize_email(email),
            password     = password,
            username     = username,
            profile_pic  = profile_pic,
            first_name   = first_name,
            last_name    = last_name,
            github       = github,
            bio          = bio
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email                   = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                = models.CharField(max_length=30, unique=True)
    first_name              = models.CharField(max_length=50, blank=True, null=True)
    last_name               = models.CharField(max_length=50, blank=True, null=True)
    profile_pic             = models.TextField(blank=True, null=True)
    bio                     = models.TextField(blank=True, null=True)
    github                  = models.CharField(max_length=100, blank=True, null=True)
    date_joined             = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)
    #subscriptions           = models.ManyToManyField('self', symmetrical=False, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj = None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True
    
    '''def count_subscriptions(self):
        return self.subscriptions.count()
    
    def count_subscribers(self):
        return Account.objects.filter(subscriptions=self).count()'''

@receiver(post_save, sender = settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
