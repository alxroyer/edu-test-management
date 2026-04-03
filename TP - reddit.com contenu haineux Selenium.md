# **TP : Test de l'IHM de Reddit avec Selenium et Intégration Continue**

Source : https://chat.mistral.ai/, sous réserve de confirmation des informations.

**Objectif** : Vérifier l’absence de contenu haineux dans les 10 derniers posts publiés sur Reddit, avec suivi des résultats via une CI.

---

## **1. Introduction**

Dans ce TP, vous allez :

- Automatiser des tests sur l’interface de Reddit avec Selenium.
- Configurer une intégration continue (CI) avec GitHub Actions.
- Visualiser l’évolution des résultats des tests via un tableau de bord graphique.

---

## **2. Prérequis**

- Un compte GitHub.
- Python 3.x installé.
- Les bibliothèques Python suivantes : `selenium`, `pytest`, `pytest-html`, `matplotlib`.
- Un navigateur (Chrome ou Firefox) et le driver correspondant (chromedriver/geckodriver).
- Un compte Reddit (optionnel, pour accéder à des fonctionnalités spécifiques).

---

## **3. Mise en place du projet**

### **3.1. Initialisation du dépôt GitHub**

1. Créez un nouveau dépôt GitHub nommé `tp-selenium-reddit`.
2. Clonez-le localement :
  ```bash
   git clone https://github.com/votre-utilisateur/tp-selenium-reddit.git
   cd tp-selenium-reddit
  ```

### **3.2. Structure du projet**

```
tp-selenium-reddit/
├── tests/
│   ├── __init__.py
│   ├── test_reddit.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
└── README.md
```

### **3.3. Installation des dépendances**

Créez un fichier `requirements.txt` :

```
selenium==4.10.0
pytest==7.4.0
pytest-html==3.2.0
matplotlib==3.7.2
```

Installez-les avec :

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## **4. Rédaction des tests Selenium**

### **4.1. Scénario de test**

Vous allez écrire **3 tests distincts** pour vérifier l’absence de contenu haineux dans les 10 derniers posts d’un subreddit (par exemple, r/all ou r/popular).

#### **Test 1 : Vérifier l’absence de mots-clés haineux dans les titres des posts**

- **Objectif** : Parcourir les 10 derniers posts et vérifier qu’aucun titre ne contient de mots-clés haineux (ex : "haine", "racisme", "insulte").
- **Résultat** : OK si aucun mot-clé n’est trouvé, KO sinon.

#### **Test 2 : Vérifier l’absence de mots-clés haineux dans les corps des posts**

- **Objectif** : Ouvrir chaque post et vérifier que le corps du texte ne contient pas de mots-clés haineux.
- **Résultat** : OK si aucun mot-clé n’est trouvé, KO sinon.

#### **Test 3 : Vérifier la présence d’un système de signalement**

- **Objectif** : Vérifier que chaque post dispose d’un bouton "Signaler".
- **Résultat** : OK si le bouton est présent pour tous les posts, KO sinon.

---

### **4.2. Exemple de code pour `test_reddit.py`**

```python
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Liste de mots-clés haineux à détecter
HATE_KEYWORDS = ["haine", "racisme", "insulte", "violence"]

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.reddit.com/r/all/")
    yield driver
    driver.quit()

def test_titres_sans_contenu_haineux(driver):
    """Vérifie l'absence de mots-clés haineux dans les titres des 10 derniers posts."""
    posts = driver.find_elements(By.CSS_SELECTOR, "[data-testid='post-title']")[:10]
    preuves = []
    for post in posts:
        preuves.append(f"Titre vérifié : {post.text}")
        title = post.text.lower()
        assert not any(keyword in title for keyword in HATE_KEYWORDS), f"Titre haineux détecté : {title}"
    # Ajoute les preuves au rapport via un attribut pytest
    pytest.titres_verifies = preuves

def test_corps_sans_contenu_haineux(driver):
    """Vérifie l'absence de mots-clés haineux dans les corps des 10 derniers posts."""
    posts = driver.find_elements(By.CSS_SELECTOR, "[data-testid='post-title']")[:10]
    preuves = []
    for post in posts:
        post.click()
        body_element = driver.find_element(By.CSS_SELECTOR, "[data-testid='post-content']")
        preuves.append(f"Corps vérifié : {body_element.text[:100]}...")  # On troncature pour éviter les logs trop longs
        body = body_element.text.lower()
        assert not any(keyword in body for keyword in HATE_KEYWORDS), f"Corps haineux détecté : {body}"
        driver.back()
    # Ajoute les preuves au rapport via un attribut pytest
    pytest.corps_verifies = preuves

def test_bouton_signalement_present(driver):
    """Vérifie la présence d'un bouton de signalement pour chaque post."""
    posts = driver.find_elements(By.CSS_SELECTOR, "[data-testid='post-title']")[:10]
    preuves = []
    for post in posts:
        post.click()
        bouton = driver.find_elements(By.CSS_SELECTOR, "[aria-label='Signaler']")
        preuves.append(f"Post : {post.text[:50]}... -> Bouton {bouton.text!r} présent")
        assert len(bouton) > 0, f"Bouton de signalement manquant pour : {post.text}"
        driver.back()
    # Ajoute les preuves au rapport via un attribut pytest
    pytest.boutons_verifies = preuves

# Hook pytest pour ajouter les preuves au rapport HTML
def pytest_html_results_table_row(report, cells):
    if report.when == "call":
        if hasattr(pytest, 'titres_verifies') and report.nodeid.endswith("test_titres_sans_contenu_haineux"):
            cellules_preuves = "<br>".join(pytest.titres_verifies)
            cells.insert(2, f"<td>{cellules_preuves}</td>")
            cells[1] = "<th>Preuves (titres)</th>"
        elif hasattr(pytest, 'corps_verifies') and report.nodeid.endswith("test_corps_sans_contenu_haineux"):
            cellules_preuves = "<br>".join(pytest.corps_verifies)
            cells.insert(2, f"<td>{cellules_preuves}</td>")
            cells[1] = "<th>Preuves (corps)</th>"
        elif hasattr(pytest, 'boutons_verifies') and report.nodeid.endswith("test_bouton_signalement_present"):
            cellules_preuves = "<br>".join(pytest.boutons_verifies)
            cells.insert(2, f"<td>{cellules_preuves}</td>")
            cells[1] = "<th>Preuves (boutons)</th>"
```

---

## **5. Configuration de l’intégration continue (CI)**

### **5.1. Création du fichier de workflow GitHub Actions**

Créez `.github/workflows/ci.yml` :

```yaml
name: CI - Tests Selenium Reddit

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest tests/ --html=report.html
      - name: Upload test report
        uses: actions/upload-artifact@v3
        with:
          name: test-report
          path: report.html
```

### **5.2. Génération d’un rapport visuel**

- Après chaque exécution des tests, un rapport HTML (`report.html`) est généré et stocké comme artefact.
- Pour visualiser l’évolution des résultats, utilisez un outil comme **GitHub Pages** ou un script Python pour générer un graphique à partir des résultats des tests (ex : nombre de tests OK/KO par campagne).

---

## **6. Suivi graphique des résultats**

### **6.1. Script de génération de graphique**

Ajoutez un script `generate_chart.py` :

```python
import matplotlib.pyplot as plt
import json

# Exemple de données (à remplacer par la récupération des résultats réels)
results = [
    {"date": "2026-04-01", "ok": 3, "ko": 0},
    {"date": "2026-04-02", "ok": 2, "ko": 1},
    {"date": "2026-04-03", "ok": 3, "ko": 0}
]

dates = [r["date"] for r in results]
ok = [r["ok"] for r in results]
ko = [r["ko"] for r in results]

plt.plot(dates, ok, label="Tests OK", marker="o")
plt.plot(dates, ko, label="Tests KO", marker="x")
plt.xlabel("Date")
plt.ylabel("Nombre de tests")
plt.title("Évolution des résultats des tests")
plt.legend()
plt.savefig("test_results.png")
```

### **6.2. Intégration dans la CI**

Modifiez `ci.yml` pour exécuter le script après les tests :

```yaml
- name: Generate chart
  run: python generate_chart.py
- name: Upload chart
  uses: actions/upload-artifact@v3
  with:
    name: test-chart
    path: test_results.png
```

---

## **7. Exécution**

1. **Forkez** ce dépôt et clonez-le localement.
2. **Complétez** les tests dans `test_reddit.py` pour couvrir les 3 scénarios.
3. **Poussez** vos modifications sur GitHub pour déclencher la CI.
4. **Analysez** les rapports HTML et le graphique générés pour suivre l’évolution des résultats.

---

## **8. Livrables attendus**

- Un dépôt GitHub contenant :
  - Les tests Selenium fonctionnels.
  - Le fichier de workflow CI configuré.
  - Un rapport HTML et un graphique des résultats.
- Un compte-rendu expliquant les résultats obtenus et les éventuelles améliorations possibles.

---

## **9. Critères d’évaluation**

- **Fonctionnalité** : Les 3 tests sont implémentés et fonctionnels.
- **CI** : La CI est configurée et génère des rapports.
- **Visualisation** : Le graphique est généré et reflète l’évolution des résultats.
- **Clarté** : Le code est commenté et le dépôt est bien organisé.
