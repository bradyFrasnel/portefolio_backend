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
        if obj.imageTechnologie:
            if obj.imageTechnologie.startswith('http'):
                return obj.imageTechnologie
            else:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.imageTechnologie)
        return None

class ProjectSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les projets avec URLs complètes"""
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = [
            'id', 'project_name', 'project_description', 'technology_used', 
            'project_image', 'image_url', 'github_link', 'demo_link', 'date_creation'
        ]
    
    def get_image_url(self, obj):
        if not obj.project_image:
            return None
        url = obj.project_image.url
        if url.startswith(('http://', 'https://')):
            return url
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(url)
        return url
