from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Project, Category, Technology, Contact, ImageProjet

class ProjectModelTest(TestCase):
    """Tests pour le modèle Project"""
    
    def setUp(self):
        """Configuration initiale pour les tests de projet"""
        self.category = Category.objects.create(name="Web", slug="web")
        self.technology = Technology.objects.create(name="Python")
        self.project = Project.objects.create(
            titre="Test Project",
            slug="test-project",
            description_courte="Short description",
            description_longue="Long description",
            categorie=self.category
        )
        self.project.technologies.add(self.technology)
    
    def test_project_creation(self):
        """Test la création d'un projet"""
        self.assertEqual(self.project.titre, "Test Project")
        self.assertEqual(self.project.slug, "test-project")
        self.assertTrue(self.project.est_publie)
        self.assertEqual(self.project.categorie.name, "Web")
        self.assertEqual(self.project.technologies.count(), 1)
    
    def test_project_str_method(self):
        """Test la méthode __str__ du projet"""
        self.assertEqual(str(self.project), "Test Project")

class CategoryModelTest(TestCase):
    """Tests pour le modèle Category"""
    
    def setUp(self):
        """Configuration initiale pour les tests de catégorie"""
        self.category = Category.objects.create(name="Mobile", slug="mobile")
    
    def test_category_creation(self):
        """Test la création d'une catégorie"""
        self.assertEqual(self.category.name, "Mobile")
        self.assertEqual(self.category.slug, "mobile")
    
    def test_category_str_method(self):
        """Test la méthode __str__ de la catégorie"""
        self.assertEqual(str(self.category), "Mobile")

class TechnologyModelTest(TestCase):
    """Tests pour le modèle Technology"""
    
    def setUp(self):
        """Configuration initiale pour les tests de technologie"""
        self.technology = Technology.objects.create(name="React")
    
    def test_technology_creation(self):
        """Test la création d'une technologie"""
        self.assertEqual(self.technology.name, "React")
    
    def test_technology_str_method(self):
        """Test la méthode __str__ de la technologie"""
        self.assertEqual(str(self.technology), "React")

class ContactModelTest(TestCase):
    """Tests pour le modèle Contact"""
    
    def setUp(self):
        """Configuration initiale pour les tests de contact"""
        self.contact = Contact.objects.create(
            nom="John Doe",
            email="john@example.com",
            type_projet="site_vitrine",
            message="I need a website"
        )
    
    def test_contact_creation(self):
        """Test la création d'un message de contact"""
        self.assertEqual(self.contact.nom, "John Doe")
        self.assertEqual(self.contact.email, "john@example.com")
        self.assertEqual(self.contact.type_projet, "site_vitrine")
        self.assertFalse(self.contact.traite)
    
    def test_contact_str_method(self):
        """Test la méthode __str__ du contact"""
        expected = f"Message de {self.contact.nom} - {self.contact.date_envoi}"
        self.assertEqual(str(self.contact), expected)

class ProjectAPITest(APITestCase):
    """Tests pour l'API des projets"""
    
    def setUp(self):
        """Configuration initiale pour les tests API de projets"""
        self.category = Category.objects.create(name="Web", slug="web")
        self.technology = Technology.objects.create(name="Python")
        self.project = Project.objects.create(
            titre="API Test Project",
            slug="api-test-project",
            description_courte="Short description",
            description_longue="Long description",
            categorie=self.category
        )
        self.project.technologies.add(self.technology)
        
        # Créer un utilisateur admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
    
    def test_get_projects_list(self):
        """Test la récupération de la liste des projets"""
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_project_detail(self):
        """Test la récupération des détails d'un projet"""
        url = reverse('project-detail', kwargs={'slug': 'api-test-project'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['titre'], "API Test Project")
    
    def test_create_project_unauthorized(self):
        """Test la création d'un projet sans authentification"""
        url = reverse('project-list')
        data = {
            'titre': 'New Project',
            'slug': 'new-project',
            'description_courte': 'Short desc',
            'description_longue': 'Long desc',
            'categorie_id': self.category.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_project_authorized(self):
        """Test la création d'un projet avec authentification admin"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('project-list')
        data = {
            'titre': 'New Project',
            'slug': 'new-project',
            'description_courte': 'Short desc',
            'description_longue': 'Long desc',
            'categorie_id': self.category.id,
            'technologies_ids': [self.technology.id]
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

class CategoryAPITest(APITestCase):
    """Tests pour l'API des catégories"""
    
    def setUp(self):
        """Configuration initiale pour les tests API de catégories"""
        self.category = Category.objects.create(name="Web", slug="web")
    
    def test_get_categories_list(self):
        """Test la récupération de la liste des catégories"""
        url = reverse('category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_category_detail(self):
        """Test la récupération des détails d'une catégorie"""
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Web")

class TechnologyAPITest(APITestCase):
    """Tests pour l'API des technologies"""
    
    def setUp(self):
        """Configuration initiale pour les tests API de technologies"""
        self.technology = Technology.objects.create(name="Python")
    
    def test_get_technologies_list(self):
        """Test la récupération de la liste des technologies"""
        url = reverse('technology-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class ContactAPITest(APITestCase):
    """Tests pour l'API des contacts"""
    
    def setUp(self):
        """Configuration initiale pour les tests API de contacts"""
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
    
    def test_create_contact_public(self):
        """Test la création d'un message de contact (publique)"""
        url = reverse('contact-list')
        data = {
            'nom': 'John Doe',
            'email': 'john@example.com',
            'type_projet': 'site_vitrine',
            'message': 'I need a website'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 1)
    
    def test_get_contacts_unauthorized(self):
        """Test la récupération des contacts sans authentification"""
        url = reverse('contact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_contacts_authorized(self):
        """Test la récupération des contacts avec authentification"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('contact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
