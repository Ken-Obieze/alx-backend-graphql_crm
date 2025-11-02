import requests
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional GraphQL ping
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql",
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        result = client.execute(query)
        if result.get("hello"):
            message += "GraphQL hello responded: " + result["hello"] + "\n"
    except Exception as e:
        message += f"GraphQL ping failed: {e}\n"

    with open("/tmp/crm_heartbeat_log.txt", "a") as log:
        log.write(message)


def update_low_stock():
    query = """
    mutation {
      updateLowStockProducts {
        updatedProducts
        message
      }
    }
    """

    try:
        response = requests.post("http://localhost:8000/graphql", json={"query": query})
        data = response.json()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("/tmp/low_stock_updates_log.txt", "a") as log:
            log.write(f"\n{timestamp} - {data['data']['updateLowStockProducts']['message']}\n")
            for product in data['data']['updateLowStockProducts']['updatedProducts']:
                log.write(f"{product}\n")

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as log:
            log.write(f"\n{datetime.now()} - Error: {e}\n")