# **TP : Test de l'IHM de Reddit avec Cucumber/Gherkin et Intégration Continue**

Source : https://chat.mistral.ai/, sous réserve de confirmation des informations.
Reprise de [TP - reddit.com Selenium.md](TP%20-%20reddit.com%20Selenium.md) avec Cucumber/Gherkin.

### **Fichier Feature : détection_contenu_haineux.feature**
```gherkin
# language: fr
Fonctionnalité: Détection de contenu haineux sur reddit.com
  En tant qu'utilisateur ou modérateur de reddit,
  Je veux pouvoir détecter automatiquement les commentaires ou posts haineux,
  Afin de modérer efficacement le contenu et maintenir un environnement sain.

  Contexte:
    Etant donné que je suis connecté à reddit.com avec un compte modérateur
    Et que je suis sur la page d'un subreddit cible

  Scénario: Détection d'un commentaire haineux
    Etant donné qu'un nouveau commentaire contenant des mots-clés haineux est posté
    Quand je lance le script de détection
    Alors le commentaire est signalé comme haineux
    Et un rapport est généré avec le lien vers le commentaire

  Scénario: Absence de contenu haineux
    Etant donné qu'un nouveau commentaire neutre est posté
    Quand je lance le script de détection
    Alors aucun signalement n'est effectué
    Et le rapport indique "Aucun contenu haineux détecté"

  Scénario: Gestion de plusieurs commentaires
    Etant donné qu'une liste de 10 commentaires est affichée sur la page
    Quand je lance le script de détection sur tous les commentaires
    Alors seuls les commentaires contenant des mots-clés haineux sont signalés
    Et le rapport liste tous les commentaires signalés avec leur position

  Exemples: Liste de mots-clés haineux
    | mot-clé    |
    | "insulte"  |
    | "haine"    |
    | "menace"   |
```

---

### **Structure du projet (exemple en Java)**

- **src/test/resources/fr/reddit/detection_contenu_haineux.feature** : le fichier Gherkin ci-dessus.
- **src/test/java/fr/reddit/steps/DetectionContenuHaineuxSteps.java** : implémentation des steps en Java avec Selenium.
- **pom.xml** : dépendances Maven pour Cucumber, Selenium, JUnit.

---

### **Exemple d'implémentation des Steps (Java)**

```java
public class DetectionContenuHaineuxSteps {
    private WebDriver driver;
    private RedditPage redditPage;

    @Given("que je suis connecté à reddit.com avec un compte modérateur")
    public void jeSuisConnecteReddit() {
        driver = new ChromeDriver();
        redditPage = new RedditPage(driver);
        redditPage.login("mod_username", "mod_password");
    }

    @When("je lance le script de détection")
    public void lancerDetection() {
        redditPage.detecterContenuHaineux();
    }

    @Then("le commentaire est signalé comme haineux")
    public void commentaireSignale() {
        assertTrue(redditPage.estCommentaireSignale());
    }

    // Autres méthodes pour les autres steps...
}
```

---

### **Bonnes pratiques à suivre**

- **Page Object Model (POM)** : Isoler la logique d'interaction avec les pages Reddit dans des classes dédiées (ex: `RedditPage`).
- **Data Tables** : Utiliser des tables de données dans Gherkin pour gérer plusieurs mots-clés ou scénarios similaires.
- **Tags** : Ajouter des tags (@smoke, @regression) pour organiser les tests.
- **Rapport** : Configurer Cucumber pour générer des rapports HTML ou JSON après exécution.

---

### **Pourquoi cette approche ?**

- **Lisibilité** : Les scénarios sont compréhensibles par tous (techniques et non-techniques).
- **Maintenabilité** : Séparation claire entre la logique métier (Gherkin) et l'implémentation technique (Java/Selenium).
- **Réutilisabilité** : Les steps peuvent être réutilisés pour d'autres fonctionnalités de modération.

---

Tu peux adapter les mots-clés haineux et les actions selon tes besoins. Veux-tu que je détaille un point spécifique (ex: implémentation des steps, configuration Maven, ou gestion des rapports) ?{"query": "exemple implémentation Cucumber Java Selenium Page Object Model"}
