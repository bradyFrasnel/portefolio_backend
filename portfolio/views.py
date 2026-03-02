from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Category, Technology, Contact
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .serializers import ProjectSerializer, CategorySerializer, TechnologySerializer, ContactSerializer

# Vues existantes...

from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour les projets.
    - Lecture publique pour tous les projets publiés
    - Écriture réservée aux administrateurs
    """
    queryset = Project.objects.filter(est_publie=True).order_by('-date_creation')
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    
    # Désactiver CSRF pour le développement
    authentication_classes = []
    
    # Filtres et recherche
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titre', 'description', 'technologie']
    ordering_fields = ['date_creation', 'titre']
    
    def get_queryset(self):
        """Optimisation des requêtes"""
        return Project.objects.filter(est_publie=True).order_by('-date_creation')

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Point de terminaison API pour les catégories (lecture seule).
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    
    # Filtres et recherche
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Point de terminaison API pour les technologies (lecture seule).
    """
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer
    permission_classes = [permissions.AllowAny]
    
    # Filtres et recherche
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class ContactViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour les messages de contact.
    - Lecture réservée aux administrateurs
    - Création autorisée pour tous (formulaire de contact)
    - Modification/Suppression réservée aux administrateurs
    """
    queryset = Contact.objects.all().order_by('-date_envoi')
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filtres et recherche
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['type_projet', 'traite']
    search_fields = ['nom', 'email', 'message']
    ordering_fields = ['date_envoi', 'nom']
    
    def get_permissions(self):
        """Permissions personnalisées selon l'action"""
        if self.action == 'create':
            # Tout le monde peut créer un message de contact
            return [permissions.AllowAny()]
        elif self.action in ['list', 'retrieve']:
            # Seuls les utilisateurs authentifiés peuvent voir les messages
            return [IsAuthenticatedOrReadOnly()]
        else:
            # Seuls les administrateurs peuvent modifier/supprimer
            return [IsAdminOrReadOnly()]
