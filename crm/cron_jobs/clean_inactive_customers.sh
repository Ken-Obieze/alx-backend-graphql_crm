#!/bin/bash

# Run Django shell command to delete inactive customers
python manage.py shell << END
from crm.models import Customer, Order
from datetime import timedelta
from django.utils import timezone

one_year_ago = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.exclude(order__order_date__gte=one_year_ago).distinct()
count = inactive_customers.count()
inactive_customers.delete()

with open("/tmp/customer_cleanup_log.txt", "a") as log:
    log.write(f"{timezone.now()} - Deleted {count} inactive customers\n")

print("Cleanup complete")
END