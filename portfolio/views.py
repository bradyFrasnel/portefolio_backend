from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Category, Technology, Contact
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import ProjectSerializer, CategorySerializer, TechnologySerializer, ContactSerializer

# Vues existantes...

from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour les projets.
    - Lecture publique pour tous les projets publiés
    - Écriture réservée aux administrateurs
    """
    queryset = Project.objects.filter(est_publie=True).order_by('ordre_affichage', '-date_creation')
    serializer_class = ProjectSerializer
    lookup_field = 'slug'
    permission_classes = [IsAdminOrReadOnly]
    
    # Filtres et recherche
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categorie', 'technologies']
    search_fields = ['titre', 'description_courte', 'description_longue']
    ordering_fields = ['date_creation', 'ordre_affichage', 'titre']
    
    def get_queryset(self):
        """Optimisation des requêtes avec select_related et prefetch_related"""
        return Project.objects.filter(est_publie=True).order_by('ordre_affichage', '-date_creation')\
            .select_related('categorie')\
            .prefetch_related('technologies', 'galerie_images')

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

@api_view(['POST'])
@permission_classes([AllowAny])
def AdminLoginView(request):
    """
    Vue d'authentification pour l'interface admin Vue.js
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        if user.is_staff:
            login(request, user)
            return Response({
                'success': True,
                'message': 'Authentification réussie',
                'user': {
                    'username': user.username,
                    'is_staff': user.is_staff
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Accès refusé : utilisateur non administrateur'
            }, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({
            'success': False,
            'message': 'Identifiants incorrects'
        }, status=status.HTTP_401_UNAUTHORIZED)
