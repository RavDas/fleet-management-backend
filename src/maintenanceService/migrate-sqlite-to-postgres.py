#!/usr/bin/env python
"""
SQLite to PostgreSQL Migration Script
Migrates data from instance/maintenance.db to PostgreSQL
"""

import sqlite3
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

def get_db_params():
    """Extract database parameters from DATABASE_URL"""
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5440/maintenance_db')
    
    # Simple parsing
    db_url = db_url.replace('postgresql://', '')
    
    # Extract components
    parts = db_url.split('@')
    user_pass = parts[0].split(':')
    host_db = parts[1].split('/')
    host_port = host_db[0].split(':')
    
    return {
        'host': host_port[0],
        'port': host_port[1] if len(host_port) > 1 else '5432',
        'database': host_db[1],
        'user': user_pass[0],
        'password': user_pass[1]
    }

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    print("=" * 60)
    print("📦 SQLite to PostgreSQL Migration")
    print("=" * 60)
    print()
    
    sqlite_db = 'instance/maintenance.db'
    
    # Check if SQLite database exists
    if not os.path.exists(sqlite_db):
        print(f"❌ SQLite database not found at: {sqlite_db}")
        print("Nothing to migrate.")
        return False
    
    try:
        # Connect to SQLite
        print("📂 Connecting to SQLite database...")
        sqlite_conn = sqlite3.connect(sqlite_db)
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        
        # Get data from SQLite
        sqlite_cursor.execute("SELECT * FROM maintenance_items")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print("⚠️  No data found in SQLite database.")
            sqlite_conn.close()
            return True
        
        print(f"✅ Found {len(rows)} records in SQLite database")
        print()
        
        # Connect to PostgreSQL
        print("📡 Connecting to PostgreSQL database...")
        db_params = get_db_params()
        pg_conn = psycopg2.connect(**db_params)
        pg_cursor = pg_conn.cursor()
        
        print("✅ Connected to PostgreSQL")
        print()
        
        # Migrate each record
        print("🔄 Migrating records...")
        migrated_count = 0
        skipped_count = 0
        
        for row in rows:
            try:
                # Convert SQLite row to dict
                data = dict(row)
                
                # Check if record already exists
                pg_cursor.execute(
                    "SELECT id FROM maintenance_items WHERE id = %s",
                    (data['id'],)
                )
                
                if pg_cursor.fetchone():
                    print(f"   ⏭️  Skipping {data['id']} (already exists)")
                    skipped_count += 1
                    continue
                
                # Insert into PostgreSQL
                pg_cursor.execute("""
                    INSERT INTO maintenance_items (
                        id, vehicle_id, type, description, status, priority,
                        due_date, scheduled_date, completed_date, created_at, updated_at,
                        current_mileage, due_mileage, estimated_cost, actual_cost,
                        assigned_to, assigned_technician, notes, parts_needed, attachments
                    ) VALUES (
                        %(id)s, %(vehicle_id)s, %(type)s, %(description)s, %(status)s, %(priority)s,
                        %(due_date)s, %(scheduled_date)s, %(completed_date)s, %(created_at)s, %(updated_at)s,
                        %(current_mileage)s, %(due_mileage)s, %(estimated_cost)s, %(actual_cost)s,
                        %(assigned_to)s, %(assigned_technician)s, %(notes)s, %(parts_needed)s, %(attachments)s
                    )
                """, data)
                
                print(f"   ✅ Migrated {data['id']} - {data['type']}")
                migrated_count += 1
                
            except Exception as e:
                print(f"   ❌ Error migrating {data.get('id', 'unknown')}: {e}")
                continue
        
        # Commit changes
        pg_conn.commit()
        
        # Close connections
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()
        
        print()
        print("=" * 60)
        print("✅ Migration Complete!")
        print("=" * 60)
        print(f"📊 Total records in SQLite: {len(rows)}")
        print(f"✅ Records migrated: {migrated_count}")
        print(f"⏭️  Records skipped (already exist): {skipped_count}")
        print()
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
        return False
        
    except psycopg2.Error as e:
        print(f"❌ PostgreSQL error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print()
    print("🔄 This script will migrate data from SQLite to PostgreSQL")
    print()
    print("⚠️  Important:")
    print("   1. Make sure PostgreSQL is running (docker-compose up postgres-maintenance)")
    print("   2. The PostgreSQL database schema should already exist")
    print("   3. Existing records in PostgreSQL will be preserved (no duplicates)")
    print()
    
    response = input("Continue with migration? (yes/no): ")
    
    if response.lower() not in ['yes', 'y']:
        print("Migration cancelled.")
        return
    
    print()
    success = migrate_data()
    
    if success:
        print("💡 Next steps:")
        print("   1. Verify data: docker exec -it postgres-maintenance psql -U postgres -d maintenance_db")
        print("   2. Run: SELECT * FROM maintenance_items;")
        print("   3. Consider backing up the SQLite database: cp instance/maintenance.db instance/maintenance.db.backup")
        print()

if __name__ == "__main__":
    main()


