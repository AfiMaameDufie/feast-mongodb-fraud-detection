from django.db import models


class Transaction(models.Model):
    transaction_id = models.CharField(max_length=64, unique=True)
    # Must stay an integer to match the Feast entity (`user_id`, INT64).
    user_id = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    is_fraudulent = models.BooleanField(default=False)

    class Meta:
        db_table = 'transactions'
        indexes = [
            # `transaction_id` is already indexed by its unique constraint.
            models.Index(fields=['user_id']),
            models.Index(fields=['timestamp']),
        ]

    def __str__(self):
        return f"Transaction {self.transaction_id} - Amount: {self.amount} - Fraudulent: {self.is_fraudulent}"