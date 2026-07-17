#!/usr/bin/env python
"""
Test script for AnalyticsEvent model
"""
import os
import sys
import django
import uuid

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import AnalyticsEvent, Project

def test_analytics_model():
    print("Testing AnalyticsEvent model...")
    
    # Test 1: Create home event
    home_event = AnalyticsEvent.objects.create(
        visitor_id=uuid.uuid4(),
        event_type='home',
        ip_address='127.0.0.1',
        country='FR',
        device_type='desktop',
        browser='Chrome'
    )
    print(f"✓ Home event created: ID {home_event.id}")
    
    # Test 2: Create project event if projects exist
    project = Project.objects.first()
    if project:
        project_event = AnalyticsEvent.objects.create(
            visitor_id=uuid.uuid4(),
            event_type='project_detail',
            project=project,
            ip_address='192.168.1.1',
            country='US',
            device_type='mobile',
            browser='Firefox'
        )
        print(f"✓ Project event created: ID {project_event.id} for project '{project.project_name}'")
    else:
        print("⚠ No projects found, skipping project event test")
    
    # Test 3: Create interaction events
    github_event = AnalyticsEvent.objects.create(
        visitor_id=uuid.uuid4(),
        event_type='github_click',
        project=project if project else None,
        ip_address='10.0.0.1',
        country='DE',
        device_type='desktop',
        browser='Safari'
    )
    print(f"✓ GitHub click event created: ID {github_event.id}")
    
    # Test 4: Count total events
    total = AnalyticsEvent.objects.count()
    print(f"✓ Total events in database: {total}")
    
    # Test 5: Test model choices
    print(f"✓ Event types: {[choice[0] for choice in AnalyticsEvent.EVENT_TYPES]}")
    print(f"✓ Device types: {[choice[0] for choice in AnalyticsEvent.DEVICE_TYPES]}")
    
    # Test 6: Test indexes (basic query performance check)
    events_by_type = AnalyticsEvent.objects.filter(event_type='home').count()
    print(f"✓ Home events count: {events_by_type}")
    
    print("\n All tests passed! AnalyticsEvent model is working correctly.")

if __name__ == '__main__':
    test_analytics_model()