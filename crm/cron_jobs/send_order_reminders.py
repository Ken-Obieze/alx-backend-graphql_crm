from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timedelta

# Setup GraphQL transport
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date range
one_week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

# Define GraphQL query
query = gql(f"""
query {{
  orders(orderDate_Gte: "{one_week_ago}") {{
    edges {{
      node {{
        id
        customer {{
          email
        }}
      }}
    }}
  }}
}}
""")

# Execute query
response = client.execute(query)

# Log results
with open("/tmp/order_reminders_log.txt", "a") as log:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log.write(f"\n{timestamp} - Order Reminders:\n")
    for edge in response["orders"]["edges"]:
        order = edge["node"]
        log.write(f"Order ID: {order['id']}, Email: {order['customer']['email']}\n")

print("Order reminders processed!")
