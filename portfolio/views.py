from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Technology, User as PortfolioUser
from .serializers import ProjectSerializer, TechnologySerializer, UserSerializer

# Vues existantes...

from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour les utilisateurs
    - Création publique (pour l'admin)
    - Lecture réservée aux admins
    """
    queryset = PortfolioUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Temporaire pour créer l'admin
    
    def create(self, request, *args, **kwargs):
        """Créer un utilisateur avec mot de passe hashé"""
        data = request.data.copy()
        
        return Response(
            {
                "success": False,
                "message": "Endpoint désactivé : utilisez /api/admin/login/ (Token DRF) avec un admin Django.",
            },
            status=status.HTTP_410_GONE,
        )
        
    def list(self, request, *args, **kwargs):
        """Lister tous les utilisateurs avec debug info"""
        users = self.queryset
        serializer = self.get_serializer(users, many=True)
        
        # Debug info
        debug_info = []
        for user in users:
            debug_info.append({
                'username': user.username,
                'password_length': len(user.password) if user.password else 0,
                'password_empty': not bool(user.password),
                'role': user.role
            })
        
        return Response({
            'users': serializer.data,
            'debug': debug_info
        })

class AdminLoginView(APIView):
    """
    Vue pour l'authentification des administrateurs
    """
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if not user or not getattr(user, "is_staff", False):
            return Response(
                {
                    "success": False,
                    "message": "Identifiants invalides ou utilisateur non autorisé",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "success": True,
                "message": "Authentification réussie",
                "user": {"username": user.username, "is_staff": bool(user.is_staff)},
                "token": token.key,
            },
            status=status.HTTP_200_OK,
        )
    
    def get(self, request):
        # Simple vérification - pas de session
        return Response({
            'success': False,
            'message': 'Utiliser POST pour se connecter'
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour les projets.
    - Lecture publique pour tous les projets
    - Écriture réservée aux administrateurs
    """
    queryset = Project.objects.all().order_by('-date_creation')
    serializer_class = ProjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    # Filtres et recherche
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['project_name', 'project_description', 'technology_used']
    ordering_fields = ['date_creation', 'project_name']
    
    def get_queryset(self):
        """Optimisation des requêtes"""
        return Project.objects.all().order_by('-date_creation')

class TechnologyViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour les technologies.
    - Lecture publique
    - Écriture réservée aux administrateurs
    """
    queryset = Technology.objects.all().order_by('nom')
    serializer_class = TechnologySerializer
    permission_classes = [IsAdminOrReadOnly]

    # Filtres et recherche
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom']
