from django.db import models

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
    # Stocké sur Cloudinary via DEFAULT_FILE_STORAGE (django-cloudinary-storage)
    project_image = models.ImageField(upload_to="projects/main/", blank=True, null=True)
    github_link = models.URLField(blank=True, null=True, help_text="Lien vers le repository GitHub")
    demo_link = models.URLField(blank=True, null=True, help_text="Lien vers la démo en ligne")
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return self.project_name
