import requests

BASE_URL = "https://dummyjson.com"


def get_products(limit=10, skip=0):
    if limit < 1 or limit > 100:
        raise ValueError("Limit must be between 1 and 100")
    if skip < 0:
        raise ValueError("Skip cannot be negative")
    response = requests.get(
        f"{BASE_URL}/products",
        params={"limit": limit, "skip": skip},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def search_products(query, limit=10):
    if not query or not str(query).strip():
        raise ValueError("Query cannot be empty")
    if limit < 1:
        raise ValueError("Limit must be positive")
    response = requests.get(
        f"{BASE_URL}/products/search",
        params={"q": query, "limit": limit},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()


def get_product_by_id(product_id):
    if not isinstance(product_id, int) or product_id <= 0:
        raise ValueError("Product ID must be a positive integer")
    response = requests.get(f"{BASE_URL}/products/{product_id}", timeout=5)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


def add_product(title, price, category="smartphones"):
    if not title or price <= 0:
        raise ValueError("Title is required and price must be positive")
    payload = {"title": title, "price": price, "category": category}
    response = requests.post(
        f"{BASE_URL}/products/add",
        json=payload,
        timeout=5,
    )
    response.raise_for_status()
    return response.json()