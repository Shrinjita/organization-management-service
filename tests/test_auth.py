import pytest
from fastapi.testclient import TestClient

def test_admin_login_success(test_client: TestClient, sample_organization_data: dict):
    """Test successful admin login"""
    # First create an organization
    test_client.post("/org/create", json=sample_organization_data)
    
    # Test login
    response = test_client.post("/admin/login", json={
        "email": sample_organization_data["email"],
        "password": sample_organization_data["password"]
    })
    
    assert response.status_code == 200
    data = response.json()
    
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert "organization_id" in data
    assert "admin_id" in data

def test_admin_login_invalid_credentials(test_client: TestClient, sample_organization_data: dict):
    """Test login with invalid credentials"""
    # Create organization
    test_client.post("/org/create", json=sample_organization_data)
    
    # Test with wrong password
    response = test_client.post("/admin/login", json={
        "email": sample_organization_data["email"],
        "password": "WrongPassword"
    })
    
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()
    
    # Test with non-existent email
    response = test_client.post("/admin/login", json={
        "email": "nonexistent@email.com",
        "password": "SomePassword"
    })
    
    assert response.status_code == 401

def test_token_verification(test_client: TestClient, sample_organization_data: dict):
    """Test JWT token verification"""
    # Create organization and login
    test_client.post("/org/create", json=sample_organization_data)
    login_response = test_client.post("/admin/login", json={
        "email": sample_organization_data["email"],
        "password": sample_organization_data["password"]
    })
    token = login_response.json()["access_token"]
    
    # Verify token
    headers = {"Authorization": f"Bearer {token}"}
    response = test_client.get("/admin/verify", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Token is valid"
    assert "admin" in data

def test_token_verification_invalid_token(test_client: TestClient):
    """Test token verification with invalid token"""
    headers = {"Authorization": "Bearer invalid_token_here"}
    response = test_client.get("/admin/verify", headers=headers)
    
    assert response.status_code == 401

def test_token_verification_missing_token(test_client: TestClient):
    """Test token verification without token"""
    response = test_client.get("/admin/verify")
    
    assert response.status_code == 403

def test_health_check(test_client: TestClient):
    """Test health check endpoint"""
    response = test_client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "database" in data

def test_root_endpoint(test_client: TestClient):
    """Test root endpoint"""
    response = test_client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "healthy"