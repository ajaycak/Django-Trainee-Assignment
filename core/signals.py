import time
import threading
import django.dispatch
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item, AuditLog



# define a custom signal for Q1 & Q2
my_signal = django.dispatch.Signal()

def slow_receiver(sender, **kwargs):
    print("Receiver thread:", threading.current_thread().name)
    print("Receiver started")
    time.sleep(3)
    print("Receiver finished")

my_signal.connect(slow_receiver)


# 4) connect a model signal receiver

@receiver(post_save,sender=Item)
def log_item_created(sender,instance,created,**kwargs):
    print("signal reciever thread",threading.current_thread().name)
    if created:
        print("creating auditlog inside reciever", threading.current_thread().name)
        AuditLog.objects.create(message=f"Item {instance.id} created")


