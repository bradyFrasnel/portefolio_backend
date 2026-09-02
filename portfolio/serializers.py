from rest_framework import serializers
from django.conf import settings
from .models import Project, Technology, ContactMessage, AnalyticsEvent


class ContactMessageSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les messages de contact"""
    class Meta:
        model = ContactMessage
        fields = ['id', 'nom', 'email', 'type_projet', 'message', 'created_at', 'is_read']
        read_only_fields = ['id', 'created_at', 'is_read']


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
    """SǸrialiseur pour les projets avec URLs Cloudinary propres"""
    image_url = serializers.SerializerMethodField()
    technologies_details = TechnologySerializer(source='technologies', many=True, read_only=True)
    technologies = serializers.PrimaryKeyRelatedField(
        queryset=Technology.objects.all(),
        many=True,
        write_only=True,
        required=False
    )

    class Meta:
        model = Project
        fields = [
            'id', 'project_name', 'project_description', 'technologies', 'technologies_details',
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

class AnalyticsEventSerializer(serializers.ModelSerializer):
    """Serializer pour AnalyticsEvent"""
    
    class Meta:
        model = AnalyticsEvent
        fields = [
            'id', 'visitor_id', 'event_type', 'timestamp',
            'project', 'country', 'browser', 'device_type'
        ]
        read_only_fields = ['id', 'timestamp', 'country']

