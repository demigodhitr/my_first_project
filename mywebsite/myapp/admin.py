from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class AccountInfoInline(admin.StackedInline):
    model = AccountInfo
    can_delete = True

class DepositInline(admin.StackedInline):
    model = Deposit
    can_delete = True
    extra = 0

class WithdrawalRequestInline(admin.StackedInline):
    model = WithdrawalRequest
    can_delete = True
    extra = 0

class NotificationsInline(admin.StackedInline):
    model = newNotifications
    can_delete = True
    extra = 0

class IDME_Inline(admin.StackedInline):
    model = IDME
    can_delete = True
    extra = 0

class CustomUserAdmin(UserAdmin):
    inlines = [AccountInfoInline, NotificationsInline, WithdrawalRequestInline, DepositInline, IDME_Inline]
# Register your models here.

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(WalletAddress)
admin.site.register(ClientMessages)