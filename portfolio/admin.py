from django.contrib import admin
from .models import Project, Contact

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les projets"""
    list_display = ('titre', 'technologie', 'date_creation', 'est_publie')
    list_filter = ('est_publie', 'technologie')
    search_fields = ('titre', 'description', 'technologie')
    readonly_fields = ('slug',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les contacts"""
    list_display = ('nom', 'email', 'type_projet', 'date_envoi', 'traite')
    list_filter = ('traite', 'type_projet')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('date_envoi',)
