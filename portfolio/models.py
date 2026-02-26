from django.db import models

class Technology(models.Model):
    """Modèle pour les technologies utilisées dans les projets"""
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='technologies/', blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    """Modèle pour les catégories de projets"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class ImageProjet(models.Model):
    """Modèle pour les images additionnelles des projets"""
    image = models.ImageField(upload_to='projects/gallery/')
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image {self.id}"

class Project(models.Model):
    """Modèle principal pour les projets du portfolio"""
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    image_principale = models.ImageField(upload_to='projects/main/')
    technologie = models.CharField(max_length=200, default='', help_text="Technologie principale utilisée")
    lien_github = models.URLField(blank=True)
    lien_demo = models.URLField(blank=True)
    date_creation = models.DateField(auto_now_add=True)
    date_mise_a_jour = models.DateField(auto_now=True)
    est_publie = models.BooleanField(default=True)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre
    
    def save(self, *args, **kwargs):
        # Générer le slug automatiquement à partir du titre
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.titre)
            slug = base_slug
            counter = 1
            # S'assurer que le slug est unique
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class Contact(models.Model):
    """Modèle pour les messages de contact"""
    TYPES_PROJET = [
        ('site_vitrine', 'Site Vitrine'),
        ('app_web', 'Application Web'),
        ('script', 'Script / Automatisation'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=100)
    email = models.EmailField()
    type_projet = models.CharField(max_length=50, choices=TYPES_PROJET)
    budget = models.CharField(max_length=100, blank=True)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)

    def __str__(self):
        return f"Message de {self.nom} - {self.date_envoi}"
