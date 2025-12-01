import threading
import time
import django.dispatch
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, AuditLog
from django.db import transaction

# Custom signal for earlier Q1 and Q2
my_signal = django.dispatch.Signal()

def slow_receiver(sender, **kwargs):
    print("Receiver thread:", threading.current_thread().name)
    print("Receiver started")
    time.sleep(3)
    print("Receiver finished")

my_signal.connect(slow_receiver)

# Transaction-aware receiver for Q3
@receiver(post_save, sender=Item)
def log_item_created(sender, instance, created, **kwargs):
    print("Signal receiver thread:", threading.current_thread().name)
    if created:
        print("Creating AuditLog inside on_commit callback")
        def callback():
            AuditLog.objects.create(message=f"Item {instance.name} created")
        transaction.on_commit(callback)
