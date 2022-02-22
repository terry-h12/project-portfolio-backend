from django.contrib import admin
from Account.models import Account
from django.contrib import admin

class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined')

admin.site.register(Account, AccountAdmin)
