"""
Service Supabase pour le projet Portfolio
Permet d'interagir directement avec Supabase en plus de Django
"""

import os
from supabase import create_client, Client
from decouple import config

class SupabaseService:
    """Service pour interagir avec Supabase"""
    
    def __init__(self):
        self.supabase_url = config('SUPABASE_URL')
        self.supabase_key = config('SUPABASE_ANON_KEY')
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
    
    def get_client(self) -> Client:
        """Retourne le client Supabase"""
        return self.supabase
    
    # Méthodes pour les projets
    def get_projects(self):
        """Récupérer tous les projets"""
        return self.supabase.table('projects').select('*').order('date_creation', desc=True).execute()
    
    def create_project(self, project_data):
        """Créer un nouveau projet"""
        return self.supabase.table('projects').insert(project_data).execute()
    
    def update_project(self, project_id: int, project_data):
        """Mettre à jour un projet"""
        return self.supabase.table('projects').update(project_data).eq('id', project_id).execute()
    
    def delete_project(self, project_id: int):
        """Supprimer un projet"""
        return self.supabase.table('projects').delete().eq('id', project_id).execute()
    
    # Méthodes pour les technologies
    def get_technologies(self):
        """Récupérer toutes les technologies"""
        return self.supabase.table('technologies').select('*').order('nom').execute()
    
    def create_technology(self, technology_data):
        """Créer une nouvelle technologie"""
        return self.supabase.table('technologies').insert(technology_data).execute()
    
    def update_technology(self, technology_id: int, technology_data):
        """Mettre à jour une technologie"""
        return self.supabase.table('technologies').update(technology_data).eq('id', technology_id).execute()
    
    def delete_technology(self, technology_id: int):
        """Supprimer une technologie"""
        return self.supabase.table('technologies').delete().eq('id', technology_id).execute()

# Instance globale du service
supabase_service = SupabaseService()
