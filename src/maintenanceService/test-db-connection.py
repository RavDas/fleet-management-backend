#!/usr/bin/env python
"""
Test Database Connection Script
Verifies PostgreSQL connection and displays sample data
"""

import os
import sys
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables
load_dotenv()

def get_db_params():
    """Extract database parameters from DATABASE_URL"""
    db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5434/maintenance_db')
    
    # Simple parsing (for more robust parsing, use urllib.parse)
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

def test_connection():
    """Test database connection"""
    print("=" * 50)
    print("🔍 Testing Maintenance Service Database Connection")
    print("=" * 50)
    print()
    
    try:
        # Get database parameters
        db_params = get_db_params()
        
        print(f"📡 Connecting to PostgreSQL...")
        print(f"   Host: {db_params['host']}")
        print(f"   Port: {db_params['port']}")
        print(f"   Database: {db_params['database']}")
        print(f"   User: {db_params['user']}")
        print()
        
        # Connect to database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        print("✅ Connection successful!")
        print()
        
        # Test 1: Check PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📦 PostgreSQL Version:")
        print(f"   {version['version'].split(',')[0]}")
        print()
        
        # Test 2: List tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"📊 Tables in database:")
        if tables:
            for table in tables:
                print(f"   ✓ {table['table_name']}")
        else:
            print("   ⚠️  No tables found. Run init-db.sql to create schema.")
        print()
        
        # Test 3: Check maintenance_items table
        if any(t['table_name'] == 'maintenance_items' for t in tables):
            cursor.execute("SELECT COUNT(*) as count FROM maintenance_items;")
            count = cursor.fetchone()
            print(f"🔧 Maintenance Items:")
            print(f"   Total records: {count['count']}")
            print()
            
            # Test 4: Show sample data
            if count['count'] > 0:
                cursor.execute("""
                    SELECT id, vehicle_id, type, status, priority, due_date 
                    FROM maintenance_items 
                    LIMIT 5;
                """)
                items = cursor.fetchall()
                
                print(f"📋 Sample Data (first 5 items):")
                print("-" * 80)
                for item in items:
                    print(f"   ID: {item['id']}")
                    print(f"   Vehicle: {item['vehicle_id']}")
                    print(f"   Type: {item['type']}")
                    print(f"   Status: {item['status']} | Priority: {item['priority']}")
                    print(f"   Due Date: {item['due_date']}")
                    print("-" * 80)
                print()
            
            # Test 5: Status summary
            cursor.execute("""
                SELECT status, COUNT(*) as count 
                FROM maintenance_items 
                GROUP BY status 
                ORDER BY count DESC;
            """)
            summary = cursor.fetchall()
            
            print(f"📊 Status Summary:")
            for row in summary:
                print(f"   {row['status']}: {row['count']} item(s)")
            print()
        
        # Close connection
        cursor.close()
        conn.close()
        
        print("=" * 50)
        print("✅ All database tests passed!")
        print("=" * 50)
        print()
        print("🚀 Next steps:")
        print("   1. Start the service: docker-compose up")
        print("   2. Test API: curl http://localhost:5001/health")
        print("   3. View data: curl http://localhost:5001/api/maintenance/")
        print()
        
        return True
        
    except psycopg2.OperationalError as e:
        print("❌ Connection failed!")
        print(f"Error: {e}")
        print()
        print("🔧 Troubleshooting:")
        print("   1. Is PostgreSQL container running?")
        print("      docker ps")
        print("   2. Start the database:")
        print("      docker-compose up -d postgres-maintenance")
        print("   3. Wait ~10 seconds for initialization")
        print("   4. Check database logs:")
        print("      docker-compose logs postgres-maintenance")
        print()
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print()
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)


