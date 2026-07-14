#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def verify_table_structure():
    """Verify the analytics_events table structure and indexes"""
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT tablename FROM pg_tables 
            WHERE tablename = 'analytics_events'
        """)
        table_exists = len(cursor.fetchall()) > 0
        print(f"✓ analytics_events table exists: {table_exists}")
        
        if table_exists:
            # Check table columns
            cursor.execute("""
                SELECT column_name, data_type, is_nullable 
                FROM information_schema.columns 
                WHERE table_name = 'analytics_events'
                ORDER BY ordinal_position
            """)
            columns = cursor.fetchall()
            print(f"✓ Table has {len(columns)} columns:")
            for col_name, data_type, nullable in columns:
                print(f"  - {col_name}: {data_type} ({'nullable' if nullable == 'YES' else 'not null'})")
            
            # Check indexes
            cursor.execute("""
                SELECT indexname FROM pg_indexes 
                WHERE tablename = 'analytics_events'
            """)
            indexes = cursor.fetchall()
            print(f"✓ Table has {len(indexes)} indexes:")
            for idx in indexes:
                print(f"  - {idx[0]}")
                
            # Check foreign key constraints
            cursor.execute("""
                SELECT conname, pg_get_constraintdef(c.oid)
                FROM pg_constraint c
                JOIN pg_class t ON c.conrelid = t.oid
                WHERE t.relname = 'analytics_events' AND c.contype = 'f'
            """)
            fks = cursor.fetchall()
            print(f"✓ Table has {len(fks)} foreign key constraints:")
            for fk_name, fk_def in fks:
                print(f"  - {fk_name}: {fk_def}")

if __name__ == "__main__":
    verify_table_structure()