#!/usr/bin/env python
"""
Crée un utilisateur admin (modèle portfolio.User, mot de passe hashé SHA256).
Utilisé par le build Render si la commande inclut : python create_admin.py
Idempotent : ne fait rien si les variables manquent ou si l’utilisateur existe.
"""
import hashlib
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def main() -> int:
    django.setup()

    from decouple import config
    from portfolio.models import User

    username = config("ADMIN_USERNAME", default="").strip()
    password = config("ADMIN_PASSWORD", default="")

    if not username or not password:
        print("create_admin: ADMIN_USERNAME ou ADMIN_PASSWORD absent — rien à faire.")
        return 0

    if User.objects.filter(username=username).exists():
        print(f"create_admin: l’utilisateur « {username} » existe déjà — skip.")
        return 0

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    User.objects.create(username=username, password=password_hash, role="admin")
    print(f"create_admin: utilisateur admin « {username} » créé.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
