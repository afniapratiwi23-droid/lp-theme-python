"""
WSGI Configuration for PythonAnywhere

Ganti 'username' dengan username PythonAnywhere Anda
Ganti 'theme-lp-editor' dengan nama folder project Anda
"""

import sys
import os

# ============================================
# GANTI INI SESUAI DENGAN SETUP ANDA
# ============================================
USERNAME = 'username'  # Ganti dengan username PythonAnywhere Anda
PROJECT_FOLDER = 'theme-lp-editor'  # Ganti dengan nama folder project

# Path ke project
project_home = f'/home/{USERNAME}/{PROJECT_FOLDER}'

# Add project directory to sys.path
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# ============================================
# ENVIRONMENT VARIABLES (OPSIONAL)
# ============================================
# Uncomment dan isi jika ingin set API key di server
# os.environ['GEMINI_API_KEY'] = 'AIzaSy...'

# ============================================
# IMPORT FLASK APP
# ============================================
from app import app as application

# For debugging (optional)
application.config['DEBUG'] = False
