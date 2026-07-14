import os
import sys
import django

# Ajouter le répertoire du projet au chemin python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from portfolio.models import Project, Technology

def inspect():
    print("=== INSPECTION DES PROJETS ===")
    projects = Project.objects.all()
    print(f"Nombre total de projets: {projects.count()}")
    for p in projects:
        print(f"\nID: {p.id}")
        print(f"Nom: {p.project_name}")
        print(f"Description: {p.project_description[:60]}...")
        print(f"Image: {p.project_image}")
        print(f"URL de l'image (via model field url): {p.project_image.url if p.project_image else 'Aucune'}")
        print(f"Demo Link: {p.demo_link}")
        print(f"GitHub Link: {p.github_link}")

    print("\n=== INSPECTION DES TECHNOLOGIES ===")
    techs = Technology.objects.all()
    print(f"Nombre total de technologies: {techs.count()}")
    for t in techs:
        print(f"Nom: {t.nom} | Image: {t.imageTechnologie}")

if __name__ == '__main__':
    inspect()
