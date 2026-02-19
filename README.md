# MyLife - Premium Personal OS

MyLife est une plateforme logicielle de gestion de vie personnelle, conçue pour centraliser les donnees critiques de l'utilisateur tout en offrant une interface premium et un systeme de conseil proactif base sur l'analyse de donnees.

## Presentation Technique

L'application repose sur une architecture robuste utilisant le framework Django pour le backend, couple a une base de donnees PostgreSQL pour la persistence. Le frontend est developpe avec des technologies web modernes (HTML5, Vanilla CSS, JavaScript) en mettant l'accent sur les principes de design Premium (Glassmorphism, Typographie Sora).

### Architecture Backend
- **Framework** : Django 5.0.2
- **Base de donnees** : PostgreSQL 16
- **Serveur de Production** : Gunicorn
- **Conteneurisation** : Docker & Docker Compose
- **Reverse Proxy** : Apache 2.4

## Systemes et Fonctionnalites Detaillee

### Le Conseiller Expert (Assistant Intelligent)
Le systeme d'assistance est le composant central de MyLife. Il s'agit d'un moteur de logique autonome qui analyse les interactions de l'utilisateur a travers tous les modules.
- **Moteur d'Evaluation (AdvisorBrain)** : Effectue des analyses quotidiennes sur le solde financier, le taux de completion des habitudes et le respect des echeances du calendrier.
- **Etats Emotionnels (AdvisorMood)** : Le conseiller dispose de quatre etats (Joyeux, Inquiet, Fache, Furieux) qui evoluent selon les performances de l'utilisateur. Chaque etat modifie radicalement le ton des communications.
- **Systeme de Communication (AdvisorDispatcher)** : Gere l'envoi de notifications in-app et de courriels au format HTML Premium. Ces messages sont concus pour agir comme un controleur rigoureux, capable de rappels fermes et de "caprices de message" en cas de relachement de la discipline.

### Module Finance
- Gestion complete des transactions (Revenus et Depenses).
- Categorisation intelligente avec indicateurs visuels.
- Suivi du budget mensuel avec calcul de solde en temps reel.
- Visualisation des transactions recentes sur le tableau de bord.

### Module Planning et Agenda
- Gestion des evenements avec codes couleurs personnalisables.
- Suivi des taches prioritaires (Basse, Moyenne, Haute).
- Rappels de notifications configures pour chaque evenement.
- Bilan journalier (Daily Digest) recapitulant l'activite prevue.

### Module Lifestyle
- Suivi des habitudes (Habits) avec frequences quotidiennes ou hebdomadaires.
- Journal d'humeur permettant de correler l'etat psychologique avec la productivite.
- Journalisation des logs pour le suivi de la discipline sur le long terme.

### Gestion de Projets
- Structure hierarchique : Projets, Jalons (Milestones) et Taches.
- Indicateurs de progression en pourcentage bases sur la completion des etapes.
- Interface de detail regroupant l'ensemble des indicateurs de performance du projet.

## Deploiement et Securite

### Conteneurisation Docker
Le projet est entierement dockerise, isolant le serveur d'application et la base de donnees dans des conteneurs distincts. Cela garantit une portabilite maximale et une facilite de mise a jour.

### Pipeline de Deploiement Continu (CI/CD)
Un workflow GitHub Actions automatise le deploiement sur le serveur de production (167.86.88.92). Chaque push sur la branche principale declenche les etapes suivantes :
1. Connexion SSH au serveur root.
2. Synchronisation des fichiers via Git.
3. Re-build des images Docker.
4. Redemarrage progressif des services (Zero downtime).
5. Mise a jour de la configuration du Reverse Proxy Apache.

### Securite et Acces
- **Port d'Exposition** : L'application est exposee sur le port securise 54321, invisible pour les scans standards.
- **Reverse Proxy** : Apache gere le nom de domaine `mylife.boutik237.com` et redirige le trafic vers le conteneur interne.
- **Hardening Django** : Desactivation du mode debug, activation des drapeaux de securite pour les cookies de session et CSRF.

## Installation Locale

### Pre-requis
- Python 3.12+
- PostgreSQL
- Pip (Gestionnaire de paquets Python)

### Procedures
1. Cloner le depot : `git clone https://github.com/neussi/MyLife-Mobile-App.git`
2. Creer et activer un environnement virtuel : `python -m venv venv`
3. Installer les dependances : `pip install -r backend/requirements.txt`
4. Configurer les variables d'environnement (`.env`).
5. Effectuer les migrations : `python manage.py migrate`
6. Lancer le serveur de developpement : `python manage.py runserver`
