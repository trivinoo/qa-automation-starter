try:
    import pytest
except ImportError:
    pytest = None

BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Verify that the system under test returns 200 OK and healthy status."""
    req = urllib.request.Request(f"{BASE_URL}/api/health")
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        data = json.loads(response.read().decode())
        assert data["status"] == "healthy"

def test_get_products_list():
    """Verify the product catalog API returns valid data with expected schema."""
    req = urllib.request.Request(f"{BASE_URL}/api/products")
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        products = json.loads(response.read().decode())
        assert isinstance(products, list)
        assert len(products) >= 1
        assert "name" in products[0]
        assert "price" in products[0]

def test_login_success():
    """Test positive authentication case."""
    payload = json.dumps({"email": "student@test.com", "password": "Password123!"}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/api/login",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        assert response.status == 200
        body = json.loads(response.read().decode())
        assert "token" in body
        assert body["user"] == "QA Student"

def test_login_invalid_credentials():
    """Test negative authentication case (401 response)."""
    payload = json.dumps({"email": "student@test.com", "password": "WrongPassword"}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/api/login",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        urllib.request.urlopen(req)
        assert False, "Expected HTTP 401 Unauthorized"
    except urllib.error.HTTPError as e:
        assert e.code == 401
        body = json.loads(e.read().decode())
        assert "error" in body

if __name__ == "__main__":
    print("Running QA API test suite...")
    test_health_check()
    print("✓ test_health_check passed")
    test_get_products_list()
    print("✓ test_get_products_list passed")
    test_login_success()
    print("✓ test_login_success passed")
    test_login_invalid_credentials()
    print("✓ test_login_invalid_credentials passed")
    print("\nAll 4 test scenarios passed successfully!")

