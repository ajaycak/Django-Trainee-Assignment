import threading
from django.http import HttpResponse
from .signals import my_signal
from .models import AuditLog, Item
from django.db import transaction

def test_signal_view(request):
    print("View thread:", threading.current_thread().name)
    print("Before send")
    my_signal.send(sender=None)
    print("After send")
    return HttpResponse("Check console for order and thread names")

def transaction_ok_view(request):
    print("transaction ok view thread:", threading.current_thread().name)
    with transaction.atomic():
        Item.objects.create(name="ok case")
    item_exists = Item.objects.filter(name="ok case").exists()
    auditlog_exists = AuditLog.objects.filter(message__contains="ok case").exists()
    response_text = f"Item exists: {item_exists}, AuditLog exists: {auditlog_exists}"
    return HttpResponse(response_text)

def transaction_rollback_view(request):
    print("transaction rollback view thread:", threading.current_thread().name)
    try:
        with transaction.atomic():
            Item.objects.create(name="rollback case")
            raise Exception("Forced rollback")
    except Exception as e:
        print("Exception caught:", e)
    item_exists = Item.objects.filter(name="rollback case").exists()
    auditlog_exists = AuditLog.objects.filter(message__contains="rollback case").exists()
    response_text = f"Item exists: {item_exists}, AuditLog exists: {auditlog_exists}"
    return HttpResponse(response_text)
