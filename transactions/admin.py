from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import CreditWallet, Transaction, WhiteListedIP

@admin.register(CreditWallet)
class CreditWalletAdmin(ModelAdmin):
    list_display = ('user', 'balance')


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = ('user', 'transaction_id', 'purchase_date')

@admin.register(WhiteListedIP)
class WhiteListedIPAdmin(ModelAdmin):
    list_display = ('ip_address', 'created_at')