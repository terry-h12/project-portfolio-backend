from django.db import models
from Account.models import Account
from django.utils import timezone

# Create your models here.
class Project(models.Model):
    image_url               = models.TextField(blank = True)
    account_id              = models.ForeignKey(Account, on_delete = models.CASCADE)
    title                   = models.TextField(max_length=100)
    description             = models.TextField(max_length=300)
    # is_shared               = models.ForeignKey('self', on_delete = models.CASCADE, null = True, blank = True, default = None)
    # date_completed          = models.DateTimeField()
    post_created            = models.DateTimeField(default = timezone.now)
    backend_repo            = models.CharField(max_length=100, blank=True, null=True) 
    frontend_repo           = models.CharField(max_length=100, blank=True, null=True) 
    website                 = models.CharField(max_length=100, blank=True, null=True) 
    is_public               = models.BooleanField(default=True)
    time_created            = models.DateTimeField(default = timezone.now)

    def __str__(self):
        return self.title