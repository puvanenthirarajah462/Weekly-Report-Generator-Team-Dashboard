#!/usr/bin/env python
"""
Script to create sample data for the Weekly Report Dashboard
Run this with: python manage.py shell < create_sample_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import User
from projects.models import Project

# Create team members
users_data = [
    {'username': 'alice', 'email': 'alice@example.com', 'password': 'password123'},
    {'username': 'bob', 'email': 'bob@example.com', 'password': 'password123'},
    {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'password123'},
    {'username': 'diana', 'email': 'diana@example.com', 'password': 'password123'},
]

for user_data in users_data:
    if not User.objects.filter(username=user_data['username']).exists():
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password'],
            role='team_member'
        )
        print(f"✓ Created user: {user.username}")
    else:
        print(f"✓ User already exists: {user_data['username']}")

# Create projects
projects_data = [
    {
        'name': 'Website Redesign',
        'description': 'Complete redesign of company website with new UI/UX'
    },
    {
        'name': 'Mobile App Development',
        'description': 'Build native iOS and Android mobile applications'
    },
    {
        'name': 'Backend API',
        'description': 'RESTful API development and maintenance'
    },
    {
        'name': 'Database Optimization',
        'description': 'Query optimization and indexing improvements'
    },
    {
        'name': 'DevOps Infrastructure',
        'description': 'Cloud infrastructure and CI/CD pipeline setup'
    },
]

for proj_data in projects_data:
    if not Project.objects.filter(name=proj_data['name']).exists():
        project = Project.objects.create(
            name=proj_data['name'],
            description=proj_data['description']
        )
        print(f"✓ Created project: {project.name}")
    else:
        print(f"✓ Project already exists: {proj_data['name']}")

print("\n✓ Sample data setup completed!")
