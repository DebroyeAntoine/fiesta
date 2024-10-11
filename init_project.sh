#!/bin/bash

# Créer la structure de base des dossiers
mkdir -p backend/app
mkdir -p frontend/src/components
mkdir -p kubernetes

# Fichiers backend Flask
touch backend/app/__init__.py
touch backend/app/routes.py
touch backend/wsgi.py

# Fichiers frontend React
touch frontend/src/components/App.js
touch frontend/package.json

# Fichiers Kubernetes
touch kubernetes/backend-deployment.yaml
touch kubernetes/frontend-deployment.yaml
touch kubernetes/service.yaml

# Docker Compose
touch docker-compose.yml

# Feedback
echo "Project structure initialized!"

