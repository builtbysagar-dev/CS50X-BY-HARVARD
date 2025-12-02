import sqlite3

def migrate_database():
    """Add billing_cycle column to existing subscriptions table"""
    print("Starting database migration...")
    
    try:
        conn = sqlite3.connect('finance.db')
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(subscriptions)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'billing_cycle' in columns:
            print("✓ billing_cycle column already exists. No migration needed.")
            conn.close()
            return
        
        # Add billing_cycle column with default value
        print("Adding billing_cycle column...")
        cursor.execute("""
            ALTER TABLE subscriptions 
            ADD COLUMN billing_cycle TEXT DEFAULT 'Monthly'
        """)
        
        # Update all existing records to have 'Monthly' as default
        cursor.execute("""
            UPDATE subscriptions 
            SET billing_cycle = 'Monthly' 
            WHERE billing_cycle IS NULL
        """)
        
        conn.commit()
        
        # Verify the migration
        cursor.execute("SELECT COUNT(*) FROM subscriptions WHERE billing_cycle = 'Monthly'")
        count = cursor.fetchone()[0]
        
        print(f"✓ Migration successful!")
        print(f"✓ Updated {count} existing subscription(s) with default billing cycle 'Monthly'")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    migrate_database()
