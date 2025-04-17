from django.db import models
from django.utils import timezone

class Company(models.Model):
    name = models.CharField(max_length=100)
    total_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name

class BalanceHistory(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='balance_history')
    previous_balance = models.DecimalField(max_digits=12, decimal_places=2)
    new_balance = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_amount= models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.company.name} - {self.timestamp}"
    
class User(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="users")
    name = models.CharField(max_length=255)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name