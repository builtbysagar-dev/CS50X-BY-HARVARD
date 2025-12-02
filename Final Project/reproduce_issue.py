import sqlite3
from datetime import datetime

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

try:
    conn = sqlite3.connect("finance.db")
    conn.row_factory = dict_factory
    db = conn.cursor()

    print("--- USERS ---")
    users = db.execute("SELECT * FROM users").fetchall()
    for u in users:
        print(u)

    print("\n--- SUBSCRIPTIONS ---")
    subs = db.execute("SELECT * FROM subscriptions").fetchall()
    for s in subs:
        print(s)

    print("\n--- SIMULATING DASHBOARD LOGIC ---")
    for user in users:
        user_id = user["id"]
        print(f"Checking for User ID: {user_id}")
        
        user_data = db.execute("SELECT entertainment_budget, productivity_budget FROM users WHERE id = ?", (user_id,)).fetchone()
        ent_budget = user_data["entertainment_budget"]
        prod_budget = user_data["productivity_budget"]

        user_subs = db.execute("SELECT * FROM subscriptions WHERE user_id = ? ORDER BY renewal_date", (user_id,)).fetchall()
        
        ent_spent = 0
        prod_spent = 0
        today = datetime.now().date()

        for sub in user_subs:
            print(f"  Processing sub: {sub['name']} ({sub['renewal_date']})")
            if sub["category"] == "Entertainment":
                ent_spent += sub["cost"]
            elif sub["category"] == "Productivity":
                prod_spent += sub["cost"]
            
            try:
                renewal_date = datetime.strptime(sub["renewal_date"], '%Y-%m-%d').date()
                delta = renewal_date - today
                days_remaining = delta.days
                print(f"    Days remaining: {days_remaining}")
            except ValueError as e:
                print(f"    ERROR parsing date: {sub['renewal_date']} - {e}")
            except Exception as e:
                print(f"    ERROR processing sub: {e}")

    print("\nDone.")

except Exception as e:
    print(f"CRITICAL ERROR: {e}")
finally:
    if 'conn' in locals():
        conn.close()
