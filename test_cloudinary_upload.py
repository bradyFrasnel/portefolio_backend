#!/usr/bin/env python
"""
Script pour tester l'upload Cloudinary
"""
import os
import sys
import django
from io import BytesIO
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core.files.uploadedfile import SimpleUploadedFile
from portfolio.models import Project

def create_test_image():
    """Créer une image de test"""
    # Créer une image rouge de 100x100
    img = Image.new('RGB', (100, 100), color='red')
    img_io = BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    
    return SimpleUploadedFile(
        "test_upload_file.jpg",
        img_io.getvalue(),
        content_type="image/jpeg"
    )

def test_upload():
    """Tester l'upload vers Cloudinary"""
    
    print("\n" + "="*70)
    print("🧪 TEST D'UPLOAD CLOUDINARY")
    print("="*70 + "\n")
    
    # Créer l'image de test
    print("1️⃣  Création d'une image de test...")
    test_image = create_test_image()
    print("   ✅ Image créée (100x100 pixels, rouge)\n")
    
    # Créer le projet
    print("2️⃣  Création du projet de test...")
    project = Project.objects.create(
        project_name="TEST CLOUDINARY - À SUPPRIMER",
        project_description="Projet de test pour vérifier l'upload Cloudinary",
        technology_used="Test",
        project_image=test_image
    )
    print(f"   ✅ Projet créé (ID: {project.id})\n")
    
    # Vérifier l'URL
    print("3️⃣  Vérification de l'URL de l'image...")
    image_url = str(project.project_image.url)
    print(f"   URL: {image_url}\n")
    
    # Analyser l'URL
    print("4️⃣  Analyse...")
    if 'cloudinary' in image_url.lower():
        print("   ✅ SUCCESS ! L'image est sur Cloudinary !")
        print("   🎉 Vous pouvez déployer en production en toute sécurité !\n")
        success = True
    elif image_url.startswith('/media/'):
        print("   ❌ ÉCHEC ! L'image est stockée localement !")
        print("   ⚠️  NE DÉPLOYEZ PAS en production - les images seront perdues !\n")
        print("   🔧 Actions à faire :")
        print("      1. Vérifier que CLOUDINARY_* est dans .env")
        print("      2. Vérifier que django-cloudinary-storage est installé")
        print("      3. Redémarrer le serveur Django\n")
        success = False
    else:
        print(f"   ⚠️  URL inattendue: {image_url}\n")
        success = False
    
    # Proposer de supprimer le projet de test
    print("="*70)
    print("🧹 NETTOYAGE")
    print("="*70 + "\n")
    
    # Nettoyage automatique
    print("="*70)
    print("🧹 NETTOYAGE")
    print("="*70 + "\n")
    
    project.delete()
    print("   ✅ Projet de test supprimé\n")
    
    return success

if __name__ == '__main__':
    try:
        success = test_upload()
        
        if success:
            print("\n" + "🎊"*35)
            print("\n   ✅ CLOUDINARY FONCTIONNE PARFAITEMENT !")
            print("   ✅ VOUS POUVEZ DÉPLOYER EN PRODUCTION !")
            print("\n" + "🎊"*35 + "\n")
        else:
            print("\n" + "⚠️ "*35)
            print("\n   ❌ CLOUDINARY NE FONCTIONNE PAS !")
            print("   ❌ NE DÉPLOYEZ PAS EN PRODUCTION !")
            print("\n" + "⚠️ "*35 + "\n")
            
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
