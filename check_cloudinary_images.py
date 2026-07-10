#!/usr/bin/env python
"""
Script pour vérifier quelles images sont sur Cloudinary
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Project

def check_images():
    """Vérifier l'état des images des projets"""
    
    projects = Project.objects.all()
    
    print(f"\n{'='*70}")
    print(f"📊 ÉTAT DES IMAGES - Total: {projects.count()} projets")
    print(f"{'='*70}\n")
    
    cloudinary_count = 0
    local_count = 0
    missing_count = 0
    
    for project in projects:
        if project.project_image:
            image_str = str(project.project_image)
            
            if 'cloudinary' in image_str.lower():
                status = "✅ CLOUDINARY"
                cloudinary_count += 1
            else:
                status = "⚠️  LOCAL"
                local_count += 1
                
            print(f"{status} | ID {project.id}")
            print(f"  Nom: {project.project_name}")
            print(f"  URL: {image_str[:80]}...")
            print()
        else:
            status = "❌ MANQUANTE"
            missing_count += 1
            print(f"{status} | ID {project.id}")
            print(f"  Nom: {project.project_name}")
            print(f"  URL: AUCUNE IMAGE")
            print()
    
    print(f"{'='*70}")
    print(f"📈 RÉSUMÉ :")
    print(f"  ✅ Sur Cloudinary  : {cloudinary_count}/{projects.count()}")
    print(f"  ⚠️  Locales (à risque): {local_count}/{projects.count()}")
    print(f"  ❌ Manquantes      : {missing_count}/{projects.count()}")
    print(f"{'='*70}\n")
    
    if local_count > 0:
        print("⚠️  ATTENTION : Vous avez des images locales !")
        print("   Ces images seront PERDUES lors du déploiement sur Render.")
        print("   Action requise : Ré-uploader ces images via l'interface admin.\n")
    
    if cloudinary_count == projects.count():
        print("🎉 PARFAIT ! Toutes les images sont sur Cloudinary.")
        print("   Vous pouvez déployer en production en toute sécurité !\n")
    
    return cloudinary_count, local_count, missing_count

if __name__ == '__main__':
    try:
        check_images()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
