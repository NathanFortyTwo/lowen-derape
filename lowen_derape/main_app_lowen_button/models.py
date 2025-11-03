from django.db import models

class Event(models.Model):
    reason = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.reason} ({self.amount} €)"
