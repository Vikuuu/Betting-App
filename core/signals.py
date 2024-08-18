from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transactions
from wager.models import CustomerWager


@receiver(post_save, sender=CustomerWager)
def log_bet_transaction(sender, instance, created, **kwargs):
    if created:
        Transactions.objects.create(
            user=instance.user,
            type=Transactions.TransactionType.BET,
            amount=instance.bet_amount,
            bet_id=instance,
        )
        print(f"Instance: {instance}, kwargs:{kwargs}, sender: {sender}")
