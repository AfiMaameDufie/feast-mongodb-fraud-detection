from django.db import models


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=64, unique=True)
    user_id = models.CharField(max_length=64)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    is_fraudulent = models.BooleanField(default=False)

    class Meta:
        db_table = 'transactions'
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['timestamp']),
        ]
    
    def __str__(self):
        return f"Transaction {self.transaction_id} - Amount: {self.amount} - Fraudulent: {self.is_fraudulent}"