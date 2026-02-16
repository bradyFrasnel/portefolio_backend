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
    slug = models.SlugField(unique=True)
    description_courte = models.TextField(max_length=200)
    description_longue = models.TextField()
    image_principale = models.ImageField(upload_to='projects/main/')
    galerie_images = models.ManyToManyField(ImageProjet, blank=True, related_name='projets')
    technologies = models.ManyToManyField(Technology, related_name='projets')
    categorie = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='projets')
    lien_github = models.URLField(blank=True)
    lien_demo = models.URLField(blank=True)
    date_creation = models.DateField(auto_now_add=True)
    date_mise_a_jour = models.DateField(auto_now=True)
    ordre_affichage = models.IntegerField(default=0)
    est_publie = models.BooleanField(default=True)

    def __str__(self):
        return self.titre

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
