#!/usr/bin/env python
"""
Script pour nettoyer les URLs d'images corrompues dans la base de données
"""
import os
import sys

# Configuration Django pour développement local
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_render')

try:
    import django
    django.setup()
    
    from portfolio.models import Project, Technology
    
    def fix_project_images():
        """Corriger les URLs d'images des projets"""
        projects = Project.objects.all()
        
        for project in projects:
            if project.project_image:
                # Vérifier si l'URL est corrompue
                image_str = str(project.project_image)
                
                if 'localhost:5173' in image_str or image_str.startswith('http:/'):
                    print(f"❌ Projet corrompu trouvé: {project.project_name}")
                    print(f"   URL actuelle: {image_str}")
                    
                    # Remplacer par None pour forcer le ré-upload
                    project.project_image = None
                    project.save()
                    print(f"   ✅ Nettoyé: image mise à None")
                else:
                    print(f"✅ Projet OK: {project.project_name}")
        
        print(f"\n {projects.count()} projets vérifiés")
    
    def fix_technology_images():
        """Corriger les URLs d'images des technologies"""
        technologies = Technology.objects.all()
        
        for tech in technologies:
            if tech.imageTechnologie:
                # Vérifier si l'URL est corrompue
                image_str = str(tech.imageTechnologie)
                
                if 'localhost:5173' in image_str or image_str.startswith('http:/'):
                    print(f"❌ Technologie corrompue trouvée: {tech.nom}")
                    print(f"   URL actuelle: {image_str}")
                    
                    # Remplacer par None
                    tech.imageTechnologie = None
                    tech.save()
                    print(f"   ✅ Nettoyé: image mise à None")
                else:
                    print(f"✅ Technologie OK: {tech.nom}")
        
        print(f"\n {technologies.count()} technologies vérifiées")
    
    if __name__ == '__main__':
        print("🔧 Nettoyage des URLs d'images corrompues...")
        print("=" * 50)
        
        fix_project_images()
        print("\n" + "=" * 50)
        fix_technology_images()
        
        print("\n✅ Nettoyage terminé !")
        print(" Note: Les images corrompues ont été mises à None.")
        print(" Vous devrez ré-uploader les images via l'API admin.")

except Exception as e:
    print(f"❌ Erreur: {e}")
    print("Essayez d'exécuter avec: python manage.py shell")
    print(" Puis manuellement:")
    print(" from portfolio.models import Project")
    print(" Project.objects.filter(project_image__contains='localhost').update(project_image=None)")
