from django.db import models
from users.models import Users


class WhiteListedIP(models.Model):
    ip_address = models.GenericIPAddressField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"White-listed IP address: {self.ip_address}"
    
class CreditWallet(models.Model):
    user = models.OneToOneField(Users,on_delete=models.CASCADE, related_name='credit')
    balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} have {self.total_credit} Total Credit"

class Transaction(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, blank=True)
    app_user_id = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    purchase_date = models.CharField(max_length=100)
    store = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=100, blank=True)
    region_code = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=100, blank=True)
    credit_amount = models.IntegerField(default=0)

    def __str__(self):
        return f"Transaction : {self.user.email} Status: {self.status}"
    
