from django.contrib import admin
from Account.models import Account
from django.contrib import admin
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined')
    # search_fields = ('email', 'username')
    # readonly_fields = ('date_joined', 'last_login')

    # fieldsets = ()
    # list_filter = ()
    # filter_horizontal = ()

admin.site.register(Account, AccountAdmin)