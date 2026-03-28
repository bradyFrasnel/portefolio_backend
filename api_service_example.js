// Service API pour le frontend adapté à la nouvelle structure Supabase
import axios from 'axios'

const API_BASE_URL = 'https://portefolio-backend-v0e0.onrender.com/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true // Important pour les cookies de session Django
})

export default {
  // Authentification Admin
  adminLogin(credentials) {
    return api.post('/admin/login/', credentials)
  },

  // Projets
  getProjects() {
    return api.get('/projects/')
  },
  
  getProject(id) {
    return api.get(`/projects/${id}/`)
  },

  createProject(data) {
    return api.post('/projects/', {
      project_name: data.project_name,
      project_description: data.project_description,
      technology_used: data.technology_used,
      project_image: data.project_image,
      github_link: data.github_link,
      demo_link: data.demo_link
    })
  },

  updateProject(id, data) {
    return api.put(`/projects/${id}/`, {
      project_name: data.project_name,
      project_description: data.project_description,
      technology_used: data.technology_used,
      project_image: data.project_image,
      github_link: data.github_link,
      demo_link: data.demo_link
    })
  },

  deleteProject(id) {
    return api.delete(`/projects/${id}/`)
  },
  
  // Technologies  
  getTechnologies() {
    return api.get('/technologies/')
  },

  createTechnology(data) {
    return api.post('/technologies/', {
      nom: data.nom,
      imageTechnologie: data.imageTechnologie
    })
  },

  updateTechnology(id, data) {
    return api.put(`/technologies/${id}/`, {
      nom: data.nom,
      imageTechnologie: data.imageTechnologie
    })
  },

  deleteTechnology(id) {
    return api.delete(`/technologies/${id}/`)
  }
}
