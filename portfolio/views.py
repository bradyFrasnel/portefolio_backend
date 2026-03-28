from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project, Technology, User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ProjectSerializer, TechnologySerializer, UserSerializer
import hashlib
import uuid

# Vues existantes...

from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

class UserViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour les utilisateurs
    - Création publique (pour l'admin)
    - Lecture réservée aux admins
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Temporaire pour créer l'admin
    
    def create(self, request, *args, **kwargs):
        """Créer un utilisateur avec mot de passe hashé"""
        data = request.data.copy()
        
        # Hasher le mot de passe manuellement
        if 'password' in data and data['password']:
            password_hash = hashlib.sha256(data['password'].encode()).hexdigest()
            data['password'] = password_hash
            
            print(f"Creating user with:")
            print(f"Username: {data.get('username')}")
            print(f"Password hash: {password_hash}")
        else:
            return Response({
                'success': False,
                'message': 'Le mot de passe est requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'success': True,
            'message': 'Utilisateur créé avec succès',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    
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
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            
            # Vérifier le mot de passe (hash SHA256)
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if user.password == password_hash and user.role == 'admin':
                # Créer un token manuellement (UUID4)
                token_key = str(uuid.uuid4())
                
                return Response({
                    'success': True,
                    'message': 'Authentification réussie',
                    'user': {
                        'username': user.username,
                        'role': user.role
                    },
                    'token': token_key
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': 'Identifiants invalides ou utilisateur non autorisé'
                }, status=status.HTTP_401_UNAUTHORIZED)
                
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': 'Utilisateur non trouvé'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
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
    
    # Désactiver CSRF pour le développement
    authentication_classes = []
    
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
    
    # Désactiver CSRF pour le développement
    authentication_classes = []
    
    # Filtres et recherche
    filter_backends = [filters.SearchFilter]
    search_fields = ['nom']
