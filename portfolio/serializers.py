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
    """Sérialiseur pour les projets avec relations imbriquées"""
    technologies = TechnologySerializer(many=True, read_only=True)
    technologies_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Technology.objects.all(), source='technologies'
    )
    
    categorie = CategorySerializer(read_only=True)
    categorie_id = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Category.objects.all(), source='categorie'
    )
    
    galerie_images = ImageProjetSerializer(many=True, read_only=True)
    galerie_images_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=ImageProjet.objects.all(), source='galerie_images'
    )

    class Meta:
        model = Project
        fields = [
            'id', 'titre', 'slug', 'description_courte', 'description_longue', 
            'image_principale', 'galerie_images', 'galerie_images_ids',
            'technologies', 'technologies_ids',
            'categorie', 'categorie_id',
            'lien_github', 'lien_demo', 'date_creation', 'date_mise_a_jour', 
            'ordre_affichage', 'est_publie'
        ]
        lookup_field = 'slug'

class ContactSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les contacts"""
    class Meta:
        model = Contact
        fields = '__all__'
