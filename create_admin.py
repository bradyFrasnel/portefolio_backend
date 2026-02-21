#!/usr/bin/env python
"""
Script pour créer automatiquement un superutilisateur Django
Utilisé lors du déploiement sur Render
"""
import os
import sys
from pathlib import Path

# Changer vers le répertoire du script pour s'assurer que Django peut trouver les modules
script_dir = Path(__file__).resolve().parent
os.chdir(script_dir)

# Ajouter le répertoire parent au PYTHONPATH si nécessaire
if str(script_dir) not in sys.path:
    sys.path.insert(0, str(script_dir))

import django
from django.contrib.auth import get_user_model

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()

# Remplace par tes infos
username = 'brady'
email = 'mokumabrady13@gmail.com'
password = 'brady@1234'

def create_superuser():
    """Crée un superutilisateur si il n'existe pas déjà"""
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"Superuser {username} created successfully!")
    else:
        print(f"Superuser {username} already exists.")

if __name__ == '__main__':
    create_superuser()
