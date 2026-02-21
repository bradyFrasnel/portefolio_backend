# Portfolio Backend API

Une API REST robuste et sécurisée pour la gestion d'un portfolio de projets, développée avec Django et Django REST Framework.

## 🚀 Améliorations Récemment Implémentées

### ✅ Sécurité Renforcée
- **Variables d'environnement** : Configuration sécurisée avec python-decouple
- **Permissions granulaires** : Contrôle d'accès basé sur les rôles
- **Settings de production** : Headers de sécurité activés en production
- **Secret Key protégée** : Plus d'exposition dans le code

### ✅ Performance Optimisée
- **Optimisation des requêtes** : `select_related` et `prefetch_related` implémentés
- **Pagination** : Pagination automatique sur les listes (10 items/page)
- **Filtres avancés** : Recherche et filtrage sur tous les endpoints
- **Documentation API** : Swagger/OpenAPI avec drf-spectacular

### ✅ Tests Complets
- **Tests unitaires** : Couverture complète des modèles
- **Tests d'API** : Validation des endpoints et permissions
- **Configuration pytest** : Environnement de test optimisé

## 📋 Prérequis

- Python 3.8+
- Virtual environment recommandé

## 🛠️ Installation

### 1. Cloner le projet
```bash
git clone <repository-url>
cd PortefolioBackend
```

### 2. Créer l'environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement
```bash
cp .env.example .env
# Éditer .env avec vos configurations
```

### 5. Appliquer les migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### 7. Démarrer le serveur
```bash
python manage.py runserver
```

## 🔧 Configuration

### Variables d'Environnement (.env)
```env
SECRET_KEY=votre-clé-secrète-min-50-caractères
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,votredomaine.com

CLOUDINARY_CLOUD_NAME=votre_cloud_name
CLOUDINARY_API_KEY=votre_api_key
CLOUDINARY_API_SECRET=votre_api_secret

CORS_ALLOWED_ORIGINS=http://localhost:5173,https://votre-frontend.com

# Variables pour la création automatique du superutilisateur (optionnel)
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=votre-mot-de-passe-securise
```

## 📚 Documentation API

### Endpoints Principaux

#### Projets
- `GET /api/projects/` - Lister les projets (publique)
- `POST /api/projects/` - Créer un projet (admin uniquement)
- `GET /api/projects/{slug}/` - Détails d'un projet
- `PUT/PATCH /api/projects/{slug}/` - Modifier un projet (admin)
- `DELETE /api/projects/{slug}/` - Supprimer un projet (admin)

#### Catégories
- `GET /api/categories/` - Lister les catégories (publique)
- `GET /api/categories/{id}/` - Détails d'une catégorie

#### Technologies
- `GET /api/technologies/` - Lister les technologies (publique)
- `GET /api/technologies/{id}/` - Détails d'une technologie

#### Contacts
- `GET /api/contact/` - Lister les messages (authentifié)
- `POST /api/contact/` - Envoyer un message (publique)
- `PUT/PATCH /api/contact/{id}/` - Modifier un message (admin)
- `DELETE /api/contact/{id}/` - Supprimer un message (admin)

### Documentation Interactive
- **Swagger UI** : `http://localhost:8000/docs/`
- **ReDoc** : `http://localhost:8000/redoc/`
- **Schema** : `http://localhost:8000/api/schema/`

## 🔍 Fonctionnalités Avancées

### Filtres et Recherche
```bash
# Filtrer par catégorie
GET /api/projects/?categorie=1

# Rechercher par titre
GET /api/projects/?search=python

# Trier par date
GET /api/projects/?ordering=-date_creation

# Pagination
GET /api/projects/?page=2
```

### Permissions
- **Projets** : Lecture publique, écriture admin
- **Catégories/Technologies** : Lecture seule publique
- **Contacts** : Création publique, lecture/écriture authentifiée

## 🧪 Tests

### Exécuter tous les tests
```bash
pytest
```

### Exécuter les tests avec coverage
```bash
pytest --cov=portfolio
```

### Tests spécifiques
```bash
pytest portfolio/tests.py::ProjectAPITest
```

## 📁 Structure du Projet

```
PortefolioBackend/
├── manage.py                    # Point d'entrée Django
├── requirements.txt             # Dépendances Python
├── .env.example                # Exemple de configuration
├── .gitignore                  # Fichiers ignorés par Git
├── pytest.ini                 # Configuration pytest
├── config/                     # Configuration Django
│   ├── settings.py             # Paramètres principaux
│   ├── urls.py                 # URLs principales
│   └── wsgi.py                 # Interface WSGI
└── portfolio/                  # Application principale
    ├── models.py               # Modèles de données
    ├── views.py                # Vues API avec permissions
    ├── serializers.py          # Sérialiseurs optimisés
    ├── permissions.py          # Permissions personnalisées
    ├── urls.py                 # URLs de l'application
    ├── admin.py                # Administration Django
    └── tests.py                # Tests complets
```

## 🚨 Sécurité

### Mesures Implémentées
- ✅ Variables d'environnement pour les secrets
- ✅ Headers de sécurité en production
- ✅ Permissions granulaires par endpoint
- ✅ Validation des entrées
- ✅ Protection CSRF activée

### Recommandations de Déploiement
1. Utiliser HTTPS obligatoirement
2. Configurer un reverse proxy (nginx)
3. Utiliser des variables d'environnement en production
4. Activer les logs de monitoring
5. Configurer des backups réguliers

## 🔄 Déploiement

### Production Checklist
- [ ] `DEBUG=False`
- [ ] Configurer `ALLOWED_HOSTS`
- [ ] Utiliser une base de données PostgreSQL
- [ ] Configurer Cloudinary avec les vraies credentials
- [ ] Activer les headers de sécurité
- [ ] Configurer les logs
- [ ] Mettre en place monitoring

### Commandes Utiles
```bash
# Collecter les fichiers statiques
python manage.py collectstatic

# Vérifier la configuration
python manage.py check --deploy

# Créer des migrations
python manage.py makemigrations portfolio

# Appliquer les migrations
python manage.py migrate
```

## 🤝 Contribution

1. Fork le projet
2. Créer une branche feature
3. Faire les modifications
4. Ajouter des tests
5. Soumettre une pull request

## 📄 Licence

Ce projet est sous licence MIT.
