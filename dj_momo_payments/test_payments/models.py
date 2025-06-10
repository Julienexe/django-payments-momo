from django.db import models
from decimal import Decimal
from django.urls import reverse

from payments import PurchasedItem
from payments.models import BasePayment

class Item(models.Model):
    """
    Model for items that can be purchased.
    """
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return self.name

class MomoPayment(BasePayment):
    """
    Model for Momo payment transactions.
    """
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=50, default='pending')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='momo_payments')

    def get_purchased_items(self):
        return [PurchasedItem(name=self.item.name, price=self.amount, quantity=1)]

    def get_failure_url(self):
        # Replace 'payment_failure' with your actual failure URL name or path
        return reverse('payment_failure', kwargs={'pk': self.pk})

    def get_success_url(self):
        # Replace 'payment_success' with your actual success URL name or path
        return reverse('payment_success', kwargs={'pk': self.pk})
