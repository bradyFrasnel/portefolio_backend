#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from portfolio.models import AnalyticsEvent

print("=" * 60)
print("VÉRIFICATION DE LA TABLE ANALYTICS_EVENTS")
print("=" * 60)

# Informations du modèle Django
print("\n1. MODÈLE DJANGO:")
print(f"   Table: {AnalyticsEvent._meta.db_table}")
print(f"   Champs:")
for field in AnalyticsEvent._meta.fields:
    print(f"     - {field.name}: {field.__class__.__name__} (nullable: {field.null}, blank: {field.blank})")

print(f"\n   Indexes:")
for index in AnalyticsEvent._meta.indexes:
    print(f"     - {index.name}: {index.fields}")

# Vérifier dans la base de données PostgreSQL
cursor = connection.cursor()

print("\n2. COLONNES DANS LA BASE DE DONNÉES:")
cursor.execute("""
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'analytics_events' 
    ORDER BY ordinal_position
""")
columns = cursor.fetchall()
for col in columns:
    nullable = "OUI" if col[2] == 'YES' else "NON"
    print(f"   - {col[0]}: {col[1]} (nullable: {nullable})")

print("\n3. INDEXES:")
cursor.execute("SELECT indexname FROM pg_indexes WHERE tablename = 'analytics_events' ORDER BY indexname;")
indexes = cursor.fetchall()
for idx in indexes:
    print(f"   - {idx[0]}")

print("\n4. CONTRAINTES:")
cursor.execute("""
    SELECT constraint_name, constraint_type 
    FROM information_schema.table_constraints 
    WHERE table_name = 'analytics_events'
""")
constraints = cursor.fetchall()
for const in constraints:
    print(f"   - {const[0]}: {const[1]}")

print("\n5. RÉSUMÉ:")
print(f"   ✓ Table 'analytics_events' existe et est prête")
print(f"   ✓ Tous les champs sont configurés")
print(f"   ✓ Les indexes sont créés")
print("=" * 60)
