#!/usr/bin/env python3
"""
Quick test script to test the chat endpoint
Run: python3 TEST_CHAT.py
"""

import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_chat():
    """Test the chat endpoint"""
    print("Testing chat endpoint...")
    print(f"Backend URL: {BACKEND_URL}")
    print()
    
    # Test request
    payload = {
        "message": "What is ROS 2?",
        "context": None
    }
    
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Success!")
            print(f"Response: {data.get('response', 'No response')[:200]}...")
        else:
            print("❌ Error!")
            try:
                error_data = response.json()
                print(f"Error: {error_data}")
            except:
                print(f"Error: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend. Is the server running?")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_chat()

