#!/usr/bin/env python
"""
Crée un admin Django (auth_user) + token DRF.

Utilisé sur Render via la commande release: python manage.py migrate && python create_admin.py
Idempotent : ne fait rien si les variables manquent ; met à jour le compte si déjà présent.
"""
import os
import sys

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


def main() -> int:
    django.setup()

    from decouple import config
    from django.contrib.auth import get_user_model
    from rest_framework.authtoken.models import Token

    username = config("ADMIN_USERNAME", default="").strip()
    email = config("ADMIN_EMAIL", default="").strip()
    password = config("ADMIN_PASSWORD", default="")

    if not username or not password:
        print("create_admin: ADMIN_USERNAME ou ADMIN_PASSWORD absent — rien à faire.")
        return 0

    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "is_staff": True,
            "is_superuser": True,
        },
    )

    # Mettre à jour si existant
    changed = False
    if email and getattr(user, "email", "") != email:
        user.email = email
        changed = True
    if not user.is_staff:
        user.is_staff = True
        changed = True
    if not user.is_superuser:
        user.is_superuser = True
        changed = True

    # Toujours définir le mot de passe à la valeur fournie (simplifie la rotation)
    user.set_password(password)
    changed = True

    if changed:
        user.save()

    Token.objects.get_or_create(user=user)

    if created:
        print(f"create_admin: admin Django « {username} » créé.")
    else:
        print(f"create_admin: admin Django « {username} » mis à jour.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
