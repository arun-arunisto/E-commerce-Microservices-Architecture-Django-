import requests

CATALOG_SERVICE_URL = "http://catalog-service:9001"

def fetch_product(product_id):
    response = requests.get(f"{CATALOG_SERVICE_URL}/products/{product_id}/")
    if response.status_code != 200:
        return None
    return response.json()

def reserve_stock(product_id, quantity, auth_header):
    response = requests.post(
        f"{CATALOG_SERVICE_URL}/products/{product_id}/reserve/",
        json={"quantity": quantity},
        headers={
            "Authorization":auth_header
        },
        timeout=3,
    )
    return response

