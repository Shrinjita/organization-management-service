"""
Integration tests for Organization Management Service
"""

import pytest
import time
from fastapi.testclient import TestClient
import json

def test_full_organization_lifecycle():
    """Test complete organization lifecycle: create → get → update → delete"""
    with TestClient(__import__("main").app) as client:
        # Test data
        org_data = {
            "organization_name": "LifecycleTestOrg",
            "email": "admin@lifecycletest.org",
            "password": "LifecyclePass123"
        }
        
        # 1. Create organization
        print("Step 1: Creating organization...")
        response = client.post("/org/create", json=org_data)
        assert response.status_code == 200
        created_org = response.json()
        org_id = created_org["id"]
        print(f"Created organization ID: {org_id}")
        
        # 2. Login as admin
        print("Step 2: Logging in as admin...")
        login_response = client.post("/admin/login", json={
            "email": org_data["email"],
            "password": org_data["password"]
        })
        assert login_response.status_code == 200
        token_data = login_response.json()
        token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("Login successful")
        
        # 3. Get organization details
        print("Step 3: Getting organization details...")
        get_response = client.get(
            f"/org/get?org_name={org_data['organization_name']}",
            headers=headers
        )
        assert get_response.status_code == 200
        fetched_org = get_response.json()
        assert fetched_org["id"] == org_id
        print("Organization details fetched successfully")
        
        # 4. Update organization
        print("Step 4: Updating organization...")
        update_response = client.put("/org/update", json={
            "organization_name": org_data["organization_name"],
            "new_organization_name": "UpdatedLifecycleOrg",
            "email": "newadmin@lifecycletest.org",
            "password": "NewPass456"
        }, headers=headers)
        assert update_response.status_code == 200
        print("Organization updated successfully")
        
        # 5. Login with new credentials
        print("Step 5: Logging in with new credentials...")
        new_login_response = client.post("/admin/login", json={
            "email": "newadmin@lifecycletest.org",
            "password": "NewPass456"
        })
        assert new_login_response.status_code == 200
        new_token_data = new_login_response.json()
        new_token = new_token_data["access_token"]
        new_headers = {"Authorization": f"Bearer {new_token}"}
        print("Login with new credentials successful")
        
        # 6. Delete organization
        print("Step 6: Deleting organization...")
        delete_response = client.delete("/org/delete", json={
            "organization_name": "UpdatedLifecycleOrg"
        }, headers=new_headers)
        assert delete_response.status_code == 200
        print("Organization deleted successfully")
        
        # 7. Verify organization is deleted
        print("Step 7: Verifying organization deletion...")
        verify_response = client.get(
            "/org/get?org_name=UpdatedLifecycleOrg",
            headers=new_headers
        )
        assert verify_response.status_code == 404
        print("Organization deletion verified")
        
        print("\n✅ Full organization lifecycle test completed successfully!")

def test_concurrent_organization_creation():
    """Test handling of concurrent organization creation attempts"""
    import threading
    
    results = []
    errors = []
    
    def create_org(org_name, email_suffix):
        try:
            with TestClient(__import__("main").app) as client:
                response = client.post("/org/create", json={
                    "organization_name": org_name,
                    "email": f"admin{email_suffix}@test.org",
                    "password": "TestPass123"
                })
                results.append((org_name, response.status_code))
        except Exception as e:
            errors.append(str(e))
    
    # Start concurrent creation attempts
    threads = []
    for i in range(3):
        thread = threading.Thread(
            target=create_org,
            args=(f"ConcurrentTestOrg{i}", i)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check results
    print(f"Concurrent creation results: {results}")
    print(f"Errors: {errors}")
    
    # Only one should succeed with 200, others should get 400 for duplicate
    success_count = sum(1 for _, status in results if status == 200)
    assert success_count == 3  # All should succeed since names are different
    
    print("✅ Concurrent creation test completed")

def test_error_handling():
    """Test various error scenarios"""
    with TestClient(__import__("main").app) as client:
        # Test 1: Invalid email format
        print("Test 1: Invalid email format...")
        response = client.post("/org/create", json={
            "organization_name": "TestOrg",
            "email": "invalid-email",
            "password": "TestPass123"
        })
        assert response.status_code == 422  # Validation error
        print("Invalid email correctly rejected")
        
        # Test 2: Short password
        print("Test 2: Short password...")
        response = client.post("/org/create", json={
            "organization_name": "TestOrg",
            "email": "admin@test.org",
            "password": "short"
        })
        assert response.status_code == 422
        print("Short password correctly rejected")
        
        # Test 3: Missing required field
        print("Test 3: Missing required field...")
        response = client.post("/org/create", json={
            "organization_name": "TestOrg",
            "email": "admin@test.org"
            # password missing
        })
        assert response.status_code == 422
        print("Missing field correctly rejected")
        
        # Test 4: Invalid token
        print("Test 4: Invalid JWT token...")
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/org/get?org_name=SomeOrg", headers=headers)
        assert response.status_code == 401
        print("Invalid token correctly rejected")
        
        print("\n✅ Error handling tests completed successfully!")

if __name__ == "__main__":
    # Run integration tests
    print("=" * 60)
    print("Running Integration Tests")
    print("=" * 60)
    
    test_full_organization_lifecycle()
    print("\n" + "=" * 60)
    
    test_concurrent_organization_creation()
    print("\n" + "=" * 60)
    
    test_error_handling()
    
    print("\n" + "=" * 60)
    print("✅ All integration tests passed!")