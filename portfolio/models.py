from django.db import models
import uuid

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default='user', choices=[
        ('admin', 'Admin'),
        ('user', 'User')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Évite le conflit avec public.users (ex. Supabase / autres extensions)
        db_table = "portfolio_users"
    
    def __str__(self):
        return self.username
    
    def is_authenticated(self):
        return True
    
    def is_staff(self):
        return self.role == 'admin'

class Technology(models.Model):
    """Modèle pour les technologies utilisées dans les projets"""
    nom = models.CharField(max_length=100, unique=True)
    imageTechnologie = models.URLField(blank=True, null=True, help_text="URL de l'image/icone de la technologie")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

class Project(models.Model):
    """Modèle principal pour les projets du portfolio"""
    project_name = models.CharField(max_length=200, unique=True)
    project_description = models.TextField()
    technology_used = models.TextField(help_text="Technologies utilisées (séparées par des virgules)")
    project_image = models.ImageField(upload_to="projects/main/", blank=True, null=True)
    github_link = models.URLField(blank=True, null=True, help_text="Lien vers le repository GitHub")
    demo_link = models.URLField(blank=True, null=True, help_text="Lien vers la démo en ligne")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return self.project_name


class AnalyticsEvent(models.Model):
    """
    Événement de tracking analytics pour le portfolio
    """
    EVENT_TYPES = [
        ('home', 'Home Page View'),
        ('project_detail', 'Project Detail View'),
        ('github_click', 'GitHub Link Click'),
        ('demo_click', 'Demo Link Click'),
    ]
    
    DEVICE_TYPES = [
        ('mobile', 'Mobile'),
        ('desktop', 'Desktop'),
    ]
    
    id = models.BigAutoField(primary_key=True)
    visitor_id = models.UUIDField(db_index=True, help_text="Identifiant unique du visiteur (localStorage)")
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    # Relations
    project = models.ForeignKey(
        'Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='analytics_events',
        help_text="Projet concerné (null pour home)"
    )
    
    # Données géographiques et techniques
    country = models.CharField(max_length=2, blank=True, db_index=True, help_text="Code pays ISO 3166-1 alpha-2")
    browser = models.CharField(max_length=50, blank=True)
    device_type = models.CharField(max_length=10, choices=DEVICE_TYPES, blank=True)
    ip_address = models.GenericIPAddressField(help_text="IP du visiteur (non exposée publiquement)")
    
    class Meta:
        db_table = 'analytics_events'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp', 'visitor_id'], name='idx_analytics_time_visitor'),
            models.Index(fields=['project', 'event_type'], name='idx_analytics_project_event'),
            models.Index(fields=['country'], name='idx_analytics_country'),
        ]
    
    def __str__(self):
        return f"{self.event_type} - {self.visitor_id} - {self.timestamp}"
