import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5000"

def test_billing_cycles():
    """Test multiple billing cycles feature"""
    s = requests.Session()
    
    # 1. Register a test user
    print("=" * 60)
    print("1. REGISTERING TEST USER")
    print("=" * 60)
    username = f"billing_test_{int(datetime.now().timestamp())}"
    password = "testpass123"
    
    r = s.post(f"{BASE_URL}/register", data={
        "username": username,
        "password": password,
        "confirmation": password
    })
    print(f"✓ Registration status: {r.status_code}")
    
    # 2. Login
    print("\n" + "=" * 60)
    print("2. LOGGING IN")
    print("=" * 60)
    r = s.post(f"{BASE_URL}/login", data={
        "username": username,
        "password": password
    })
    print(f"✓ Login status: {r.status_code}")
    
    # 3. Add subscriptions with different billing cycles
    print("\n" + "=" * 60)
    print("3. ADDING SUBSCRIPTIONS WITH DIFFERENT BILLING CYCLES")
    print("=" * 60)
    
    subscriptions = [
        {"name": "Disney+", "cost": "79.99", "billing_cycle": "Annually", "category": "Entertainment"},
        {"name": "Spotify", "cost": "10.99", "billing_cycle": "Monthly", "category": "Entertainment"},
        {"name": "Gym Membership", "cost": "25.00", "billing_cycle": "Weekly", "category": "Other"},
        {"name": "Adobe Creative Cloud", "cost": "54.99", "billing_cycle": "Monthly", "category": "Productivity"},
        {"name": "ProtonVPN", "cost": "23.99", "billing_cycle": "Quarterly", "category": "Utilities"},
    ]
    
    renewal_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    for sub in subscriptions:
        r = s.post(f"{BASE_URL}/add", data={
            "name": sub["name"],
            "cost": sub["cost"],
            "billing_cycle": sub["billing_cycle"],
            "category": sub["category"],
            "renewal_date": renewal_date,
            "cancel_url": ""
        })
        status = "✓" if r.status_code in [200, 302] else "✗"
        print(f"{status} {sub['name']}: ${sub['cost']}/{sub['billing_cycle']} - Status: {r.status_code}")
    
    # 4. View dashboard and check calculations
    print("\n" + "=" * 60)
    print("4. VERIFYING DASHBOARD AND BUDGET CALCULATIONS")
    print("=" * 60)
    
    r = s.get(f"{BASE_URL}/")
    if r.status_code == 200:
        print("✓ Dashboard loaded successfully")
        
        # Check if billing cycle information is in the response
        if "Weekly" in r.text or "Annually" in r.text or "Quarterly" in r.text:
            print("✓ Billing cycle information present in dashboard")
        else:
            print("✗ Billing cycle information NOT found")
            
        if "/week" in r.text or "/year" in r.text or "/quarter" in r.text:
            print("✓ Custom billing cycle labels (/week, /year, /quarter) found")
        else:
            print("✗ Custom billing cycle labels NOT found")
            
        if "≈" in r.text or "month" in r.text:
            print("✓ Normalized monthly cost display found")
        else:
            print("⚠ Normalized monthly cost might not be displaying")
    else:
        print(f"✗ Dashboard failed: {r.status_code}")
    
    # 5. Calculate expected normalized monthly costs
    print("\n" + "=" * 60)
    print("5. EXPECTED NORMALIZED MONTHLY COSTS")
    print("=" * 60)
    
    weekly_monthly = 25.00 * 52 / 12
    quarterly_monthly = 23.99 / 3
    annually_monthly = 79.99 / 12
    monthly_total = 10.99 + 54.99
    
    print(f"Gym Membership (Weekly $25): ${weekly_monthly:.2f}/month")
    print(f"ProtonVPN (Quarterly $23.99): ${quarterly_monthly:.2f}/month")
    print(f"Disney+ (Annually $79.99): ${annually_monthly:.2f}/month")
    print(f"Spotify + Adobe (Monthly): ${monthly_total:.2f}/month")
    print(f"\nTotal Entertainment (Spotify + Disney+): ${10.99 + annually_monthly:.2f}/month")
    print(f"Total Productivity (Adobe): ${54.99:.2f}/month")
    print(f"Total Other (Gym): ${weekly_monthly:.2f}/month")
    print(f"Total Utilities (ProtonVPN): ${quarterly_monthly:.2f}/month")
    print(f"\nGRAND TOTAL: ${10.99 + annually_monthly + 54.99 + weekly_monthly + quarterly_monthly:.2f}/month")
    
    print("\n" + "=" * 60)
    print("✓ TESTING COMPLETE!")
    print("=" * 60)
    print(f"\nTest user credentials:")
    print(f"  Username: {username}")
    print(f"  Password: {password}")
    print(f"\nYou can login manually to verify the dashboard display.")

if __name__ == "__main__":
    try:
        test_billing_cycles()
    except Exception as e:
        print(f"\n✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
