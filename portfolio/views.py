from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Project, Technology, ContactMessage, AnalyticsEvent
from .serializers import ProjectSerializer, TechnologySerializer, ContactMessageSerializer, AnalyticsEventSerializer
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.decorators import action

# Vues existantes...

from .permissions import IsAdminOrReadOnly, IsAuthenticatedOrReadOnly

class CleanupImageView(APIView):
    """
    Vue pour nettoyer les URLs d'images corrompues (localhost, via.placeholder.com, etc.)
    """
    permission_classes = [permissions.AllowAny]

    # Patterns d'URLs invalides à supprimer
    INVALID_PATTERNS = ['localhost', '127.0.0.1', 'via.placeholder.com', 'placeholder.com']

    def post(self, request):
        """Nettoyer les URLs d'images invalides dans les projets et technologies"""
        try:
            projects_count = 0
            techs_count = 0

            for pattern in self.INVALID_PATTERNS:
                # Nettoyer les projets
                qs = Project.objects.filter(project_image__contains=pattern)
                projects_count += qs.count()
                qs.update(project_image=None)

                # Nettoyer les technologies
                qs_tech = Technology.objects.filter(imageTechnologie__contains=pattern)
                techs_count += qs_tech.count()
                qs_tech.update(imageTechnologie=None)

            return Response({
                'success': True,
                'message': 'Nettoyage effectué',
                'projects_cleaned': projects_count,
                'technologies_cleaned': techs_count,
                'patterns_checked': self.INVALID_PATTERNS,
            })

        except Exception as e:
            return Response({
                'success': False,
                'message': f'Erreur: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """Vérifier l'état des données et compter les URLs invalides"""
        try:
            result = {
                'total_projects': Project.objects.count(),
                'total_technologies': Technology.objects.count(),
                'invalid_by_pattern': {}
            }

            for pattern in self.INVALID_PATTERNS:
                result['invalid_by_pattern'][pattern] = {
                    'projects': Project.objects.filter(project_image__contains=pattern).count(),
                    'technologies': Technology.objects.filter(imageTechnologie__contains=pattern).count(),
                }

            return Response(result)

        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.throttling import ScopedRateThrottle

class ContactMessageViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour les messages de contact.
    - Création publique
    - Lecture, modification et suppression réservées aux admins
    """
    queryset = ContactMessage.objects.all().order_by('-created_at')
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def get_throttles(self):
        if self.action == 'create':
            self.throttle_scope = 'contact'
            return [ScopedRateThrottle()]
        return super().get_throttles()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message_obj = serializer.save()
        
        import resend
        from django.conf import settings
        
        try:
            resend.api_key = getattr(settings, 'RESEND_API_KEY', '')
            
            subject = f"Nouveau message Portfolio: {message_obj.type_projet} - {message_obj.nom}"
            mail_content = f"""Nouveau message de contact recu !
            
Nom: {message_obj.nom}
Email: {message_obj.email}
Telephone: {message_obj.telephone}
Type de projet: {message_obj.type_projet}

Message:
{message_obj.message}
            """
            
            params = {
                "from": "Acme <onboarding@resend.dev>",
                "to": ["mokumabrady13@gmail.com"],
                "subject": subject,
                "text": mail_content
            }
            email = resend.Emails.send(params)
        except Exception as e:
            print("Erreur: Une erreur s'est produite", e)
            
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Vous aurez une réponse dans les plus brefs délaits. Merci pour votre message !"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

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
    
    def get_serializer_context(self):
        """Ajouter le request au contexte pour les URLs complètes"""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

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
    
    def get_serializer_context(self):
        """Ajouter le request au contexte pour les URLs complètes"""
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context

class AnalyticsEventViewSet(viewsets.ModelViewSet):
    """
    Point de terminaison API pour l'analytique.
    - Création publique (tracking)
    - Statistiques (GET) réservées aux administrateurs
    """
    queryset = AnalyticsEvent.objects.all()
    serializer_class = AnalyticsEventSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]

    def create(self, request, *args, **kwargs):
        # On copie les données pour pouvoir les modifier (notamment si c'est un QueryDict immuable)
        data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        if hasattr(data, '_mutable'):
            data._mutable = True
            
        if 'project_id' in request.data:
            data['project'] = request.data.get('project_id')
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
            
        # Par défaut si l'IP n'est pas dispo
        if not ip:
            ip = '0.0.0.0'
            
        serializer.save(ip_address=ip)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Retourne les données agrégées pour les graphiques du frontend.
        """
        # page views over time (daily)
        page_views_over_time = (
            AnalyticsEvent.objects
            .filter(event_type__in=['home', 'project_detail'])
            .annotate(date=TruncDate('timestamp'))
            .values('date')
            .annotate(views=Count('id'))
            .order_by('date')
        )
        
        # visits per project
        visits_per_project = (
            AnalyticsEvent.objects
            .filter(event_type='project_detail', project__isnull=False)
            .values('project__project_name')
            .annotate(views=Count('id'))
            .order_by('-views')
        )
        
        # external clicks
        external_clicks = (
            AnalyticsEvent.objects
            .filter(event_type__in=['github_click', 'demo_click'])
            .values('event_type')
            .annotate(clicks=Count('id'))
        )
        
        stats_data = {
            'page_views_over_time': list(page_views_over_time),
            'visits_per_project': list(visits_per_project),
            'external_clicks': list(external_clicks),
        }
        
        return Response(stats_data)
