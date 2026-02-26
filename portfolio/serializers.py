from rest_framework import serializers
from .models import Project, Category, Technology, Contact, ImageProjet

class TechnologySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les technologies"""
    class Meta:
        model = Technology
        fields = ['id', 'name', 'logo']

class CategorySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les catégories"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ImageProjetSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les images de projet"""
    class Meta:
        model = ImageProjet
        fields = ['id', 'image', 'description']

class ProjectSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les projets simplifié"""

    class Meta:
        model = Project
        fields = [
            'id', 'titre', 'slug', 'description', 'image_principale', 
            'technologie', 'lien_github', 'lien_demo', 'date_creation', 
            'date_mise_a_jour', 'est_publie'
        ]
        lookup_field = 'slug'

class ContactSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les contacts"""
    class Meta:
        model = Contact
        fields = '__all__'
