#!/usr/bin/env python
import os
import django
import uuid

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import AnalyticsEvent, Project

print("=" * 60)
print("TEST DE CRÉATION D'ÉVÉNEMENT ANALYTICS")
print("=" * 60)

# Récupérer ou créer un projet de test
try:
    project = Project.objects.first()
    if not project:
        print("Aucun projet trouvé. Création d'un projet de test...")
        project = Project.objects.create(
            project_name="Test Project for Analytics",
            project_description="Test project for analytics tracking",
            technology_used="Python, Django",
            github_link="https://github.com/test",
            demo_link="https://demo.example.com"
        )
        print(f"✓ Projet créé: {project.project_name} (ID: {project.id})")
    else:
        print(f"✓ Projet existant trouvé: {project.project_name} (ID: {project.id})")
except Exception as e:
    print(f"✗ Erreur lors de la récupération/création du projet: {e}")
    project = None

# Créer des événements de test
test_cases = [
    {
        "visitor_id": str(uuid.uuid4()),
        "event_type": "home",
        "ip_address": "192.168.1.1",
        "device_type": "desktop",
        "browser": "Chrome",
        "country": "FR"
    },
    {
        "visitor_id": str(uuid.uuid4()),
        "event_type": "project_detail",
        "ip_address": "192.168.1.2",
        "device_type": "mobile",
        "browser": "Safari",
        "country": "US",
        "project": project
    },
    {
        "visitor_id": str(uuid.uuid4()),
        "event_type": "github_click",
        "ip_address": "192.168.1.3",
        "device_type": "desktop",
        "browser": "Firefox",
        "country": "DE",
        "project": project
    },
    {
        "visitor_id": str(uuid.uuid4()),
        "event_type": "demo_click",
        "ip_address": "192.168.1.4",
        "device_type": "mobile",
        "browser": "Edge",
        "country": "UK",
        "project": project
    }
]

print("\nCréation d'événements de test:")
created_count = 0
for i, test_case in enumerate(test_cases, 1):
    try:
        event = AnalyticsEvent.objects.create(
            visitor_id=test_case["visitor_id"],
            event_type=test_case["event_type"],
            ip_address=test_case["ip_address"],
            device_type=test_case.get("device_type", ""),
            browser=test_case.get("browser", ""),
            country=test_case.get("country", ""),
            project=test_case.get("project")
        )
        print(f"  ✓ Événement {i}: {event.event_type} (visitor_id: {str(event.visitor_id)[:8]}...)")
        created_count += 1
    except Exception as e:
        print(f"  ✗ Événement {i} - Erreur: {e}")

# Vérifier les événements créés
print(f"\nVérification des événements créés:")
total_events = AnalyticsEvent.objects.count()
print(f"  Total d'événements: {total_events}")

# Statistiques par type
print(f"\n  Par type d'événement:")
for event_type, label in AnalyticsEvent.EVENT_TYPES:
    count = AnalyticsEvent.objects.filter(event_type=event_type).count()
    print(f"    - {label}: {count}")

# Statistiques par appareil
print(f"\n  Par type d'appareil:")
for device_type, label in AnalyticsEvent.DEVICE_TYPES:
    count = AnalyticsEvent.objects.filter(device_type=device_type).count()
    print(f"    - {label}: {count}")

# Pays uniques
countries = AnalyticsEvent.objects.values_list('country', flat=True).distinct()
print(f"\n  Pays uniques: {', '.join(countries)}")

print("\n" + "=" * 60)
print(f"✓ Test complété avec succès!")
print(f"  {created_count} événement(s) créé(s)")
print("=" * 60)
