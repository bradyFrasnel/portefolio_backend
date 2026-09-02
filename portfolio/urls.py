from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from .views import ProjectViewSet, TechnologyViewSet, ContactMessageViewSet, AdminLoginView, CleanupImageView, AnalyticsEventViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'technologies', TechnologyViewSet)
router.register(r'contact', ContactMessageViewSet, basename='contact')
router.register(r'analytics', AnalyticsEventViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    # Authentification admin
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    # Nettoyage des images
    path('cleanup/images/', CleanupImageView.as_view(), name='cleanup-images'),
    # Documentation API
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
