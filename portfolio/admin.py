from django.contrib import admin
from .models import Project, Category, Technology, Contact, ImageProjet

class ProjectImageInline(admin.TabularInline):
    """Inline pour les images de projet dans l'admin"""
    model = Project.galerie_images.through
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les projets"""
    list_display = ('titre', 'categorie', 'date_creation', 'est_publie', 'ordre_affichage')
    list_filter = ('categorie', 'est_publie', 'technologies')
    search_fields = ('titre', 'description_courte')
    prepopulated_fields = {'slug': ('titre',)}
    filter_horizontal = ('technologies',)
    # inlines = [ProjectImageInline] # ManyToMany inline requires intermediate model or specific handling

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les catégories"""
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les technologies"""
    list_display = ('name',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Configuration de l'admin pour les contacts"""
    list_display = ('nom', 'email', 'type_projet', 'date_envoi', 'traite')
    list_filter = ('traite', 'type_projet')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('date_envoi',)

admin.site.register(ImageProjet)
