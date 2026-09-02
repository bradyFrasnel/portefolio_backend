from django.contrib import admin
from .models import Project, Technology

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les projets"""
    list_display = ('project_name', 'date_creation')
    list_filter = ('date_creation',)
    search_fields = ('project_name', 'project_description')
    readonly_fields = ('date_creation',)

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les technologies"""
    list_display = ('nom', 'created_at')
    search_fields = ('nom',)
    readonly_fields = ('created_at',)
