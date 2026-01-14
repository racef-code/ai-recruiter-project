# 📚 Documentation - AI Smart Recruiter

Bienvenue dans la documentation complète du projet AI Smart Recruiter.

## 📋 Table des Matières

### 📖 Guides Principaux
- **[Accueil](../README.md)** - Vue d'ensemble et quick start
- **[Changelog](CHANGELOG.md)** - Historique des versions et modifications
- **[Résumé des Améliorations](IMPROVEMENTS_SUMMARY.md)** - Détails techniques des améliorations

### 🔧 Configuration
Pour configurer l'application, consultez la section Configuration du README principal.

**Fichiers de configuration:**
- `config.py` - Configuration centralisée
- `.env.example` - Template des variables d'environnement

### 🛠️ Scripts Utilitaires
Les scripts se trouvent dans le dossier `scripts/`:
- `test_improvements.py` - Tests automatisés des améliorations
- `run_test.py` - Test runner pour validation

### 📊 Architecture

#### Structure du Projet
```
llm project_recruter_ai/
├── app.py                    # Point d'entrée Streamlit
├── config.py                 # Configuration centralisée
├── logger.py                 # Système de logging
│
├── resume_matcher/           # Logique métier
│   ├── resume_parser.py      # Extraction PDF
│   ├── matcher.py            # Matching sémantique
│   └── explainer.py          # Explications IA
│
├── docs/                     # Documentation (ce dossier)
├── scripts/                  # Scripts utilitaires
├── data/                     # CVs de test
├── uploads/                  # Uploads temporaires
└── logs/                     # Logs applicatifs
```

#### Flux de Données

1. **Upload** → L'utilisateur upload des PDFs
2. **Parsing** → `resume_parser.py` extrait le texte
3. **Vectorisation** → `matcher.py` génère les embeddings (cached!)
4. **Matching** → Calcul de similarité cosinus
5. **Ranking** → Tri des candidats par score
6. **Explanation** → `explainer.py` génère l'explication (optionnel)
7. **Display** → Affichage dans Streamlit

### ⚡ Améliorations de Performance

#### Model Caching
Le modèle SentenceTransformer est chargé une seule fois grâce à `@st.cache_resource`:

**Avant:**
```python
# Rechargé à chaque interaction
model = SentenceTransformer('all-MiniLM-L6-v2')
```

**Après:**
```python
@st.cache_resource
def get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')
```

**Résultat:** 50-80% plus rapide après le premier chargement!

#### Logging Structuré
Tous les events sont loggés avec timestamp, niveau, et contexte:
```
2026-01-14 16:19:17 | INFO | matcher.py:42 | Loading model...
2026-01-14 16:19:19 | INFO | matcher.py:51 | Model loaded successfully
```

### 🧪 Tests

#### Tests Automatisés
```bash
python scripts/test_improvements.py
```

Tests effectués:
1. ✅ Configuration chargée
2. ✅ Logger fonctionnel
3. ✅ Model caching opérationnel
4. ✅ Fichiers dupliqués supprimés
5. ✅ Versions fixées

#### Tests Manuels
```bash
# 1. Lancer l'app
streamlit run app.py

# 2. Uploader des CVs
# 3. Analyser
# 4. Vérifier les logs
cat logs/app_$(date +%Y%m%d).log
```

### 📝 Logs

#### Localisation
Les logs sont dans `logs/app_YYYYMMDD.log`

#### Format
```
timestamp | level | file:line | message
```

#### Niveaux
- **DEBUG**: Détails pour debugging
- **INFO**: Événements normaux
- **WARNING**: Situations inhabituelles
- **ERROR**: Erreurs non-critiques
- **CRITICAL**: Erreurs critiques

#### Exemples
```bash
# Voir les logs du jour
cat logs/app_20260114.log

# Filtrer les erreurs
grep ERROR logs/app_20260114.log

# Suivre en temps réel
tail -f logs/app_20260114.log
```

### 🔐 Sécurité

#### Bonnes Pratiques
- ✅ Exécution locale uniquement
- ✅ Pas de données envoyées au cloud
- ✅ Variables sensibles dans `.env`
- ✅ `.env` dans `.gitignore`
- ⚠️ Validation des uploads à améliorer (Phase 2)

### 🚀 Prochaines Étapes

Consultez [IMPROVEMENTS_SUMMARY.md](IMPROVEMENTS_SUMMARY.md) section "Prochaines Étapes" pour:
- Phase 2: Optimisations performance supplémentaires
- Phase 3: Tests unitaires et qualité code
- Phase 4: Refactoring architecture
- Phase 5: Fonctionnalités bonus

### 💡 FAQ

**Q: Pourquoi l'app est lente au premier lancement?**
R: Le modèle SentenceTransformer (~80MB) se charge. Ensuite c'est rapide!

**Q: Où sont stockés les logs?**
R: Dans `logs/app_YYYYMMDD.log` avec rotation quotidienne.

**Q: Comment changer le modèle LLM?**
R: Éditez `.env` et changez `OLLAMA_MODEL=llama3` vers votre modèle.

**Q: L'app fonctionne sans Ollama?**
R: Oui! Les explications IA ne seront juste pas disponibles.

**Q: Comment contribuer?**
R: Fork, branch, commit, push, PR! Voir le README principal.

### 📞 Support

- 🐛 **Bugs**: Ouvrir une issue sur GitHub
- 💡 **Features**: Proposer via GitHub discussions
- 📧 **Questions**: Consulter cette doc ou ouvrir une issue

---

**Dernière mise à jour:** 14 Janvier 2026
