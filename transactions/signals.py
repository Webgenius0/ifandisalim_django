from django.dispatch import receiver
from django.db.models.signals import post_save
from users.models import Users
from .models import CreditWallet, WhiteListedIP


@receiver(post_save, sender=Users)
def create_credit_wallet(sender, instance, created, **kwargs):
    if created:
         # check the ip address 
        CreditWallet.objects.create(user=instance, balance=2)
        # WhiteListedIP.objects.create(ip_address=ip_address)

