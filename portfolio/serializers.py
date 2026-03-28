from rest_framework import serializers
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
    class Meta:
        model = Technology
        fields = ['id', 'nom', 'imageTechnologie', 'created_at']

class ProjectSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les projets simplifié"""

    class Meta:
        model = Project
        fields = [
            'id', 'project_name', 'project_description', 'technology_used', 
            'project_image', 'github_link', 'demo_link', 'date_creation'
        ]
