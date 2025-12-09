# Django Trainee Assignment – Signals & Transactions

This repo contains my solutions for the Django trainee assignment.  
I focused on understanding **how Django signals behave** (sync/async, threads, transactions) rather than just making the code “work”.

---

## Q1 & Q2 – Are signals synchronous and do they run in the same thread?

### What I built

- A custom signal `my_signal`.
- A receiver `slow_receiver` that:
  - prints the current thread name
  - sleeps for 3 seconds
- A view `/test-signal/` that:
  - prints the view thread name
  - calls `my_signal.send(...)`
  - prints “After send” after sending the signal.

Console output (trimmed):

<img width="794" height="211" alt="image" src="https://github.com/user-attachments/assets/9d540aa9-2ec1-467a-a808-f163e08474e2" />

### What this shows

- **Synchronous:**  
  `After send` only appears after `Receiver finished`.  
  The HTTP response is delayed by the 3‑second sleep in the receiver. If signals were async, the view would print `After send` immediately.

- **Same thread:**  
  Both the view and the receiver log the same thread name (`Thread-1 (process_request_thread)`), so the receiver runs in the same thread as the caller by default.

---

## Q3 – Do signal handlers participate in the same database transaction?

I used Django’s built‑in `post_save` signal for `Item` and attached a receiver.

For this part I wanted to see what happens when I save an Item inside a transaction.

A Django signal runs because of that save and also writes to the database.

The transaction either commits or is rolled back.

Models I used:

Item – main object I save.

AuditLog – simple log table that records when an Item is created.

Signal setup (idea, not full code):

I used Django’s built-in post_save signal on Item.

In the receiver, I register a callback with transaction.on_commit() that creates the AuditLog.

How I tested it: 

I created two views:

  /Q3-ok/

    Wrap Item.objects.create("ok case") in transaction.atomic().

    Let it complete normally.

    Check if:

        Item with name “ok case” exists.

        AuditLog message containing “ok case” exists.

  Result: Item exists: True, AuditLog exists: True

  /Q3-rollback/

    Wrap Item.objects.create("rollback case") in transaction.atomic().

    After saving, raise an exception to force a rollback.

    Catch the exception so the view can still return a response.

    Check if:

      Item with name “rollback case” exists.

      AuditLog message containing “rollback case” exists.

  Result: Item exists: False, AuditLog exists: False

And console output:
<img width="1324" height="297" alt="image" src="https://github.com/user-attachments/assets/f496baab-583c-401f-8205-23f2c3afc51a" />

and the audits:

<img width="1467" height="573" alt="image" src="https://github.com/user-attachments/assets/d1583cca-8e63-4963-b8a8-e05ac9131a69" />




