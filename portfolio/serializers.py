from rest_framework import serializers
from django.conf import settings
from .models import Project, Technology, User


class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les utilisateurs"""
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class TechnologySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les technologies"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Technology
        fields = ['id', 'nom', 'imageTechnologie', 'image_url', 'created_at']

    def get_image_url(self, obj):
        image = obj.imageTechnologie
        if not image:
            return None
        if image.startswith(('http://', 'https://')):
            # Filtrer les URLs invalides
            INVALID = ['via.placeholder.com', 'placeholder.com', 'localhost', '127.0.0.1']
            if any(p in image for p in INVALID):
                return None
            return image
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(image)
        return image


class ProjectSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les projets avec URLs Cloudinary propres"""
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id', 'project_name', 'project_description', 'technology_used',
            'project_image', 'image_url', 'github_link', 'demo_link', 'date_creation'
        ]

    def get_image_url(self, obj):
        """
        Retourne l'URL Cloudinary de l'image du projet.
        Filtre les URLs invalides (via.placeholder.com, localhost)
        pour éviter les erreurs ERR_CONNECTION_CLOSED côté frontend.
        """
        if not obj.project_image:
            return None

        try:
            url = obj.project_image.url
        except Exception:
            return None

        if not url:
            return None

        # Patterns d'URLs invalides à filtrer
        INVALID_PATTERNS = [
            'via.placeholder.com',
            'placeholder.com',
            'placeholder',
            'localhost',
            '127.0.0.1',
        ]
        for pattern in INVALID_PATTERNS:
            if pattern in url:
                return None

        # URL absolue Cloudinary (https://res.cloudinary.com/...) → retourner directement
        if url.startswith(('http://', 'https://')):
            return url

        # URL relative → construire l'URL absolue
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
        return url
