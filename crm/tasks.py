from celery import shared_task
import requests
from datetime import datetime

@shared_task
def generate_crm_report():
    query = """
    query {
      customers { totalCount }
      orders { edges { node { totalAmount } } }
    }
    """
    try:
        response = requests.post("http://localhost:8000/graphql", json={"query": query})
        data = response.json()["data"]

        total_customers = data["customers"]["totalCount"]
        orders = data["orders"]["edges"]
        total_orders = len(orders)
        total_revenue = sum(float(order["node"]["totalAmount"]) for order in orders)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

        with open("/tmp/crm_report_log.txt", "a") as log:
            log.write(report)

    except Exception as e:
        with open("/tmp/crm_report_log.txt", "a") as log:
            log.write(f"{datetime.now()} - Error: {e}\n")
