import sys
import os

# Add the project root to the system path so backend imports resolve correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.main import app
