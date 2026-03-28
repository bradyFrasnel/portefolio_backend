# GUIDE DE MIGRATION VERS SUPABASE
# ===================================

# ÉTAPE 1: CRÉATION DU PROJET SUPABASE
# ----------------------------------

1. Allez sur https://supabase.com
2. Cliquez sur "Start your project"
3. Configurez :
   - Organization: Votre nom
   - Project Name: portfolio-api
   - Database Password: [Choisissez un mot de passe fort]
   - Region: Europe West (Ireland)
4. Cliquez sur "Create new project"
5. Attendez la création (2-3 minutes)

# ÉTAPE 2: RÉCUPÉRATION DES IDENTIFIANTS
# ------------------------------------

Une fois le projet créé, allez dans Settings > API :

Notez ces informations :
- Project URL: https://[PROJECT_ID].supabase.co
- Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
- Service Role Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

Allez dans Settings > Database :
- Connection string: postgresql://postgres:[PASSWORD]@db.[PROJECT_ID].supabase.co:5432/postgres

# ÉTAPE 3: CONFIGURATION VARIABLES D'ENVIRONNEMENT
# --------------------------------------------------

Dans Render.com, ajoutez ces variables d'environnement :

SUPABASE_URL=https://[PROJECT_ID].supabase.co
SUPABASE_ANON_KEY=[VOTRE_ANON_KEY]
SUPABASE_DB_PASSWORD=[VOTRE_PASSWORD_DB]
SUPABASE_DB_HOST=db.[PROJECT_ID].supabase.co

# ÉTAPE 4: MIGRATION DES DONNÉES
# -------------------------------

## Option A: Via l'interface Supabase (Recommandée)

1. Allez dans Supabase > Table Editor
2. Créez les tables manuellement avec l'interface SQL :

```sql

-- Table Technologies  
CREATE TABLE technologies (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    imageTechnologie TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Table Projects
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(200) NOT NULL,
    project_description TEXT NOT NULL,
    technology_used TEXT NOT NULL
    project_image TEXT NOT NULL,
    github_link TEXT NOT NULL,
    demo_link TEXT NOT NULL,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
);

```

## Option B: Via Django Migrations

1. Configurez les variables d'environnement
2. Déployez sur Render
3. Les migrations Django créeront automatiquement les tables

# ÉTAPE 5: DÉPLOIEMENT ET TEST
# ---------------------------

1. Committez les changements :
```bash
git add .
git commit -m "Migrate to Supabase database"
git push origin main
```

2. Attendez le déploiement Render (2-3 minutes)

3. Testez la connexion :
```bash
# Dans le shell Render (si disponible)
python manage.py dbshell
# OU via Supabase SQL Editor
SELECT * FROM categories LIMIT 1;
```

4. Créez les données initiales :
```sql
-- Catégories
INSERT INTO categories (name, slug, description) VALUES 
('Web', 'web', 'Projets web et applications'),
('Mobile', 'mobile', 'Applications mobiles'),
('Desktop', 'desktop', 'Applications desktop');

-- Technologies
INSERT INTO technologies (name, slug, icon, level) VALUES
('Django', 'django', 'django-icon', 5),
('Vue.js', 'vuejs', 'vue-icon', 4),
('Python', 'python', 'python-icon', 5),
('Tailwind CSS', 'tailwind', 'tailwind-icon', 4);
```

# ÉTAPE 6: VÉRIFICATION FRONTEND
# --------------------------------

1. Testez l'API :
```bash
curl https://portefolio-backend-v0e0.onrender.com/api/projects/
```

2. Testez le frontend :
```bash
npm run dev
# Allez sur http://localhost:5173
```

# ÉTAPE 7: BONNES PRATIQUES SUPABASE
# -----------------------------------

## Sécurité
- Utilisez toujours l'Anon Key pour le frontend
- Utilisez le Service Role Key pour les opérations admin
- Configurez les RLS (Row Level Security) si nécessaire

## Performance
- Activez le connection pooling
- Utilisez les index sur les champs fréquemment recherchés
- Configurez le cache si nécessaire

## Backup
- Les backups sont automatiques avec Supabase
- Vous pouvez exporter les données manuellement
- Configurez les webhooks pour les événements

# DÉPANNAGE
# ---------

## Erreur de connexion
- Vérifiez les variables d'environnement
- Confirmez que le mot de passe DB est correct
- Testez la connexion string avec psql

## Erreur SSL
- Supabase nécessite SSL obligatoirement
- Vérifiez que `sslmode=require` est dans la config

## Erreur CORS
- Ajoutez votre domaine frontend dans les CORS de Supabase
- Configurez les headers correctement

# AVANTAGES DE SUPABASE
# --------------------

✅ PostgreSQL managé
✅ Interface web intuitive
✅ Backup automatiques
✅ Real-time subscriptions
✅ Authentification intégrée
✅ Storage pour fichiers
✅ Edge functions
✅ API REST automatique
✅ Documentation générée
✅ Monitoring intégré

# RÉFÉRENCES
# ----------

- Documentation Supabase: https://supabase.com/docs
- Django + Supabase: https://supabase.com/docs/guides/frameworks/django
- Connection strings: https://supabase.com/docs/reference/python
