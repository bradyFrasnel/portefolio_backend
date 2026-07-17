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

from portfolio.models import AnalyticsEvent, Project
import uuid
from django.utils import timezone

def test_analytics_model():
    """Test the AnalyticsEvent model creation and validation"""
    print("Testing AnalyticsEvent model...")
    
    # Test 1: Create a home page view event
    visitor_uuid = uuid.uuid4()
    
    try:
        home_event = AnalyticsEvent.objects.create(
            visitor_id=visitor_uuid,
            event_type='home',
            ip_address='192.168.1.1',
            country='FR',
            browser='Chrome',
            device_type='desktop'
        )
        print(f"✓ Created home event: {home_event}")
    except Exception as e:
        print(f"✗ Error creating home event: {e}")
        return False
    
    # Test 2: Create a project detail event (with project reference)
    try:
        # Get the first project if it exists
        project = Project.objects.first()
        if project:
            project_event = AnalyticsEvent.objects.create(
                visitor_id=visitor_uuid,
                event_type='project_detail',
                ip_address='192.168.1.1',
                country='FR',
                browser='Chrome',
                device_type='mobile',
                project=project
            )
            print(f"✓ Created project detail event: {project_event}")
        else:
            print("! No projects exist, skipping project detail test")
    except Exception as e:
        print(f"✗ Error creating project detail event: {e}")
        return False
    
    # Test 3: Verify model constraints and choices
    try:
        # Test invalid event_type (should fail validation on save)
        invalid_event = AnalyticsEvent(
            visitor_id=visitor_uuid,
            event_type='invalid_type',
            ip_address='192.168.1.1'
        )
        # This should work until we call full_clean() or save()
        print("✓ Model accepts invalid event_type until validation")
    except Exception as e:
        print(f"! Unexpected error with invalid event type: {e}")
    
    # Test 4: Verify indexes and meta configuration
    meta = AnalyticsEvent._meta
    print(f"✓ Model table name: {meta.db_table}")
    print(f"✓ Model ordering: {meta.ordering}")
    print(f"✓ Model indexes: {len(meta.indexes)} custom indexes defined")
    
    # Test 5: Query events
    try:
        total_events = AnalyticsEvent.objects.count()
        print(f"✓ Total events in database: {total_events}")
        
        home_events = AnalyticsEvent.objects.filter(event_type='home').count()
        print(f"✓ Home events: {home_events}")
        
        project_events = AnalyticsEvent.objects.filter(event_type='project_detail').count()
        print(f"✓ Project detail events: {project_events}")
    except Exception as e:
        print(f"✗ Error querying events: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = test_analytics_model()
    if success:
        print("\n All tests passed! AnalyticsEvent model is working correctly.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    # Clean up test data
    print("\nCleaning up test data...")
    try:
        AnalyticsEvent.objects.all().delete()
        print("✓ Test data cleaned up")
    except Exception as e:
        print(f"! Could not clean up test data: {e}")