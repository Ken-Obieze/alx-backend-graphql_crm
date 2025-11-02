import requests
from datetime import datetime, timedelta

# GraphQL endpoint
url = "http://localhost:8000/graphql"

# Calculate date range
one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# GraphQL query
query = """
query {
  orders(orderDate_Gte: "%s") {
    edges {
      node {
        id
        customer {
          email
        }
      }
    }
  }
}
""" % one_week_ago

# Send request
response = requests.post(url, json={"query": query})
data = response.json()

# Log results
with open("/tmp/order_reminders_log.txt", "a") as log:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.write(f"\n{timestamp} - Order Reminders:\n")
    for edge in data["data"]["orders"]["edges"]:
        order = edge["node"]
        log.write(f"Order ID: {order['id']}, Email: {order['customer']['email']}\n")

print("Order reminders processed!")
