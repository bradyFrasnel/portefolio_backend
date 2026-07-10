#!/usr/bin/env python
"""
Script pour nettoyer les URLs d'images corrompues dans la base de données Supabase
"""
import os
import sys
import django

# Ajouter le répertoire du projet au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Project, Technology

def clean_corrupt_urls():
    """Nettoyer les URLs corrompues dans la base de données"""
    
    print("🔍 Recherche des URLs corrompues...")
    print("=" * 60)
    
    # Nettoyer les projets
    print("\n📦 Nettoyage des projets...")
    projects = Project.objects.all()
    corrupted_projects = 0
    
    for project in projects:
        if project.project_image:
            image_str = str(project.project_image)
            
            # Détecter les URLs corrompues
            if ('localhost' in image_str.lower() or 
                image_str.startswith('http:/') or 
                image_str.startswith('https:/')):
                
                print(f"  ❌ Projet corrompu: {project.id}")
                print(f"     URL actuelle: {image_str}")
                
                project.project_image = None
                project.save()
                corrupted_projects += 1
                print(f"     ✅ Nettoyé (image mise à None)")
    
    print(f"\n  📊 {corrupted_projects}/{projects.count()} projets nettoyés")
    
    # Nettoyer les technologies
    print("\n🔧 Nettoyage des technologies...")
    technologies = Technology.objects.all()
    corrupted_techs = 0
    
    for tech in technologies:
        if tech.imageTechnologie:
            image_str = str(tech.imageTechnologie)
            
            if ('localhost' in image_str.lower() or 
                not image_str.startswith('http')):
                
                print(f"  ❌ Technologie corrompue: {tech.nom}")
                print(f"     URL actuelle: {image_str}")
                
                tech.imageTechnologie = None
                tech.save()
                corrupted_techs += 1
                print(f"     ✅ Nettoyé (image mise à None)")
    
    print(f"\n  📊 {corrupted_techs}/{technologies.count()} technologies nettoyées")
    
    print("\n" + "=" * 60)
    print("✅ Nettoyage terminé !")
    print("\n📝 Prochaines étapes :")
    print("   1. Ré-uploader les images via l'interface admin")
    print("   2. Les nouvelles images seront stockées sur Cloudinary")

if __name__ == '__main__':
    try:
        clean_corrupt_urls()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
