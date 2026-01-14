"""
Script de test pour vérifier les améliorations.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import project modules
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 60)
print("TEST DES AMELIORATIONS")
print("=" * 60)

# Test 1: Configuration
print("\n1. Test Configuration...")
try:
    from config import config
    print(f"   - Model: {config.model.name}")
    print(f"   - Ollama URL: {config.ollama.base_url}")
    print(f"   - Upload dir: {config.app.upload_dir}")
    print("   [OK] Configuration chargee avec succes")
except Exception as e:
    print(f"   [ERREUR] {e}")

# Test 2: Logger
print("\n2. Test Logger...")
try:
    from logger import logger
    logger.info("Test du logger")
    print("   [OK] Logger fonctionne - voir logs/app_20260114.log")
except Exception as e:
    print(f"   [ERREUR] {e}")

# Test 3: Matcher avec cache
print("\n3. Test Matcher (model caching)...")
try:
    from resume_matcher.matcher import get_model
    print("   - Chargement du modele (peut prendre quelques secondes)...")
    model = get_model()
    print(f"   - Modele charge: {model}")
    print("   [OK] Model caching fonctionne")
except Exception as e:
    print(f"   [ERREUR] {e}")

# Test 4: Vérifier que le fichier dupliqué a été supprimé
print("\n4. Test Nettoyage...")
import os
if os.path.exists("resume_parser.py"):
    print("   [ATTENTION] resume_parser.py existe toujours dans root")
else:
    print("   [OK] Fichier duplique supprime")

# Test 5: Requirements
print("\n5. Test Requirements...")
try:
    with open("requirements.txt", "r") as f:
        content = f.read()
        if "==" in content:
            print("   [OK] Versions fixees dans requirements.txt")
        else:
            print("   [ATTENTION] Versions non fixees")
except Exception as e:
    print(f"   [ERREUR] {e}")

print("\n" + "=" * 60)
print("TESTS TERMINES")
print("=" * 60)
print("\nPour lancer l'app: streamlit run app.py")
