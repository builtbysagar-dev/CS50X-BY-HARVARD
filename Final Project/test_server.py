import requests
import threading
import time
import os
import sys

# Start the server in a separate process/thread? 
# Actually, the user's server is running. I can just hit it.
# But I don't know the user's password.
# I can register a new user.

BASE_URL = "http://127.0.0.1:5000"

def test_server():
    s = requests.Session()
    
    # 1. Register
    print("Registering...")
    username = f"test_user_{int(time.time())}"
    password = "password"
    r = s.post(f"{BASE_URL}/register", data={
        "username": username,
        "password": password,
        "confirmation": password
    })
    print(f"Register status: {r.status_code}")
    
    # 2. Login (should be auto-logged in or redirected to login?)
    # The app redirects to login after register.
    print("Logging in...")
    r = s.post(f"{BASE_URL}/login", data={
        "username": username,
        "password": password
    })
    print(f"Login status: {r.status_code}")
    
    # 3. Access Dashboard
    print("Accessing Dashboard...")
    r = s.get(f"{BASE_URL}/")
    print(f"Dashboard status: {r.status_code}")
    if r.status_code == 500:
        print("CRITICAL: Dashboard returned 500")
        # Can't see server logs from here, but confirming the 500 is key.
    else:
        print("Dashboard loaded successfully")

if __name__ == "__main__":
    try:
        test_server()
    except Exception as e:
        print(f"Error: {e}")
