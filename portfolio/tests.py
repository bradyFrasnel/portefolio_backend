from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Project, Technology, ContactMessage

class ProjectModelTest(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            project_name="Test Project",
            project_description="Test Description",
        )
    
    def test_project_creation(self):
        self.assertEqual(self.project.project_name, "Test Project")
        self.assertEqual(self.project.project_description, "Test Description")
    
    def test_project_str_method(self):
        self.assertEqual(str(self.project), "Test Project")

class TechnologyModelTest(TestCase):
    def setUp(self):
        self.technology = Technology.objects.create(nom="Python")
    
    def test_technology_creation(self):
        self.assertEqual(self.technology.nom, "Python")
    
    def test_technology_str_method(self):
        self.assertEqual(str(self.technology), "Python")

class ContactMessageModelTest(TestCase):
    def setUp(self):
        self.contact = ContactMessage.objects.create(
            nom="John Doe",
            email="john@example.com",
            type_projet="site_vitrine",
            message="I need a website"
        )
    
    def test_contact_creation(self):
        self.assertEqual(self.contact.nom, "John Doe")
        self.assertEqual(self.contact.email, "john@example.com")
        self.assertFalse(self.contact.is_read)
    
    def test_contact_str_method(self):
        self.assertIn("John Doe", str(self.contact))

class PortfolioAPITest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.project = Project.objects.create(
            project_name="API Test Project",
            project_description="Desc",
        )
        self.technology = Technology.objects.create(nom="Django")

    # --- Projects API ---
    def test_get_projects_list(self):
        url = reverse('project-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_project_detail(self):
        url = reverse('project-detail', kwargs={'pk': self.project.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['project_name'], "API Test Project")
    
    def test_create_project_unauthorized(self):
        url = reverse('project-list')
        data = {
            'project_name': 'New Project',
            'project_description': 'Short desc',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_create_project_authorized(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('project-list')
        data = {
            'project_name': 'New Project',
            'project_description': 'Short desc',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)

    # --- Technology API ---
    def test_get_technologies_list(self):
        url = reverse('technology-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    # --- Contact API ---
    def test_create_contact_public(self):
        url = reverse('contact-list')
        data = {
            'nom': 'Jane Doe',
            'email': 'jane@example.com',
            'type_projet': 'ecommerce',
            'message': 'Hello'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Message envoyé avec succès')
        self.assertEqual(ContactMessage.objects.count(), 1)

    def test_get_contacts_unauthorized(self):
        url = reverse('contact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_contacts_authorized(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('contact-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # --- Admin Login ---
    def test_admin_login_success(self):
        url = reverse('admin-login')
        data = {'username': 'admin', 'password': 'admin123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_admin_login_invalid(self):
        url = reverse('admin-login')
        data = {'username': 'admin', 'password': 'wrongpassword'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
