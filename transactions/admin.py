from django.contrib import admin

# Register your models here.
from .models import CreditWallet, Transaction, WhiteListedIP

@admin.register(CreditWallet)
class CreditWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_id', 'purchase_date')

@admin.register(WhiteListedIP)
class WhiteListedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'created_at')