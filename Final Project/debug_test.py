from app import app

with app.test_client() as client:
    # Register a test user
    print("Testing registration...")
    response = client.post('/register', data={
        'username': 'test_debug',
        'password': 'password123',
        'confirmation': 'password123'
    }, follow_redirects=False)
    print(f"Register status: {response.status_code}")
    
    # Try to login
    print("\nTesting login...")
    try:
        response = client.post('/login', data={
            'username': 'test_debug',
            'password': 'password123'
        }, follow_redirects=False)
        print(f"Login status: {response.status_code}")
    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
    
    # Try to access dashboard
    print("\nTesting dashboard...")
    try:
        response = client.get('/', follow_redirects=False)
        print(f"Dashboard status: {response.status_code}")
    except Exception as e:
        print(f"Dashboard error: {e}")
        import traceback
        traceback.print_exc()
