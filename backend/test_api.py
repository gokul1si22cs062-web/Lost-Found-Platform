"""
Test script to verify all API endpoints are working correctly.
Run this after starting the server to verify everything works.
"""
import sys
import os

# Add site-packages to path (for D:\python.exe installation)
site_packages = r'D:\Lib\site-packages'
if os.path.exists(site_packages) and site_packages not in sys.path:
    sys.path.insert(0, site_packages)

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def print_test(name):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)

def test_root():
    print_test("Root Endpoint")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_create_post():
    print_test("Create Post")
    try:
        data = {
            "title": "Test Lost Wallet",
            "description": "Black leather wallet with credit cards",
            "location": "Library, 2nd floor",
            "date_lost_found": "2024-02-10",
            "post_type": "lost",
            "images": [],
            "user_id": "test_user_123"
        }
        response = requests.post(f"{BASE_URL}/api/posts", json=data)
        print(f"Status: {response.status_code}")
        if response.status_code == 201:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            return result.get("id")
        else:
            # Try to get error details
            try:
                error_detail = response.json()
                print(f"Error Response: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"Error Response (text): {response.text[:200]}")
            if response.status_code == 500:
                print("\n⚠️  Server error - likely MongoDB connection issue")
                print("   The API server is running, but MongoDB is not connected.")
                print("   Set up MongoDB (local or Atlas) to test post creation.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_get_all_posts():
    print_test("Get All Posts")
    try:
        response = requests.get(f"{BASE_URL}/api/posts")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Found {len(result)} posts")
        if result:
            print(f"First post: {json.dumps(result[0], indent=2)}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_single_post(post_id):
    print_test("Get Single Post")
    try:
        response = requests.get(f"{BASE_URL}/api/posts/{post_id}")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Response: {json.dumps(result, indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_search_posts():
    print_test("Search Posts")
    try:
        response = requests.get(f"{BASE_URL}/api/posts?search=wallet")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Found {len(result)} posts matching 'wallet'")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_filter_by_type():
    print_test("Filter by Post Type")
    try:
        response = requests.get(f"{BASE_URL}/api/posts?post_type=lost")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Found {len(result)} 'lost' posts")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_post(post_id):
    print_test("Update Post (Ownership Check)")
    try:
        # Test with correct owner
        data = {
            "title": "Test Lost Wallet - Updated",
            "description": "Black leather wallet with credit cards and ID"
        }
        response = requests.put(
            f"{BASE_URL}/api/posts/{post_id}?user_id=test_user_123",
            json=data
        )
        print(f"Status (correct owner): {response.status_code}")
        if response.status_code == 200:
            print(f"Updated post: {json.dumps(response.json(), indent=2)}")
        
        # Test with wrong owner (should fail)
        response2 = requests.put(
            f"{BASE_URL}/api/posts/{post_id}?user_id=wrong_user",
            json=data
        )
        print(f"Status (wrong owner): {response2.status_code}")
        print(f"Response: {response2.json()}")
        
        return response.status_code == 200 and response2.status_code == 403
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_delete_post(post_id):
    print_test("Delete Post (Ownership Check)")
    try:
        # Test with wrong owner (should fail)
        response = requests.delete(f"{BASE_URL}/api/posts/{post_id}?user_id=wrong_user")
        print(f"Status (wrong owner): {response.status_code}")
        if response.status_code == 403:
            print("✓ Correctly rejected wrong owner")
        
        # Test with correct owner
        response2 = requests.delete(f"{BASE_URL}/api/posts/{post_id}?user_id=test_user_123")
        print(f"Status (correct owner): {response2.status_code}")
        return response2.status_code == 204
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_location_search():
    print_test("Search by Location")
    try:
        response = requests.get(f"{BASE_URL}/api/posts/search/location?location=library")
        print(f"Status: {response.status_code}")
        result = response.json()
        print(f"Found {len(result)} posts in 'library'")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("LOST & FOUND PLATFORM API - VERIFICATION TEST")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the server is running: uvicorn main:app --reload")
    
    results = {}
    
    # Test 1: Root endpoint
    results["Root"] = test_root()
    
    # Test 2: Create post
    post_id = test_create_post()
    results["Create Post"] = post_id is not None
    
    if not post_id:
        print("\n❌ Failed to create post. Cannot continue with other tests.")
        print("Check if MongoDB is running and accessible.")
        return
    
    # Test 3: Get all posts
    results["Get All Posts"] = test_get_all_posts()
    
    # Test 4: Get single post
    results["Get Single Post"] = test_get_single_post(post_id)
    
    # Test 5: Search posts
    results["Search Posts"] = test_search_posts()
    
    # Test 6: Filter by type
    results["Filter by Type"] = test_filter_by_type()
    
    # Test 7: Update post
    results["Update Post"] = test_update_post(post_id)
    
    # Test 8: Location search
    results["Location Search"] = test_location_search()
    
    # Test 9: Delete post
    results["Delete Post"] = test_delete_post(post_id)
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to the server.")
        print("Make sure the server is running:")
        print("  cd backend")
        print("  uvicorn main:app --reload")

