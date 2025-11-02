from datetime import datetime
import requests

def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive\n"

    # Optional: ping GraphQL endpoint
    try:
        response = requests.post("http://localhost:8000/graphql", json={"query": "{ hello }"})
        if response.status_code == 200:
            message += "GraphQL responded successfully\n"
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