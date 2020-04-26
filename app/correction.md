# Correction.md

Ryme Berro BERR03539707

## Liste des fonctionnalités developpées 

  - ### A1 (10xp) : 
    La liste des contrevenants est obtenue en format XML à l'aide d'une requête HTTP et son contenu est stocké dans une base de données SQLite.
   Pour tester, il suffit de checker la table **contraventions** crée. cette fonctionnaliteé est implementé avec une fonction Python **LoadXML** qui telecharge les donnees et les stockent directement dans la BD.

 - ### A2 (10xp): 
    Creation d'une application Flask pour accéder aux données de la base de données. La page d’accueil offre un outil de recherche qui permet de trouver les contrevenants et affiche les resultats sur une nouvelle page. 
    Il suffit de lancer l'application et soummettre le mot clé de la recherche pour visualiser les resultats. La fonction en question est **get_contraventionsBySearch**

- ### A3 (5xp): 
    Mise en place du BackgroundScheduler dans l’application afin d’extraire les données de la ville de Montréal à chaque jour, à minuit. 
    Un message s'affiche dans le terminal lors de la mise a jour a 24h00. 

- ### A4 (10xp): 
    service REST permettant d'obtenir la liste des contrevenants ayant commis une infraction entre deux dates spécifiques.
    testé avec **Advanced Rest Client**
    pour visualiser le resultat json : 
    GET /contrevenants?du=2017-07-01&au=2017-07-10
    ou
    http://127.0.0.1:5000/contravenants?du=2017-07-01&au=2017-07-10
	 
- ### A5 (10xp):  
      Petit formulaire de recherche sur la page d'acceuil pour trouver les établissements et le nombre de contraventions obtenue durant 2 dates saisies. 

- ### A6 (10xp):
      Mode de recherche par nom du restaurant (etablissement) . La liste de tous les contrevenants est affiché dans une liste déroulante et l'utilisateur peut choisir un restaurant parmi les options.
      Lorsque la recherche est lancé, l'application affiche les information des
      différentes infractions de l'établissement

- ### C1 (10xp): 
      service REST permettant d'obtenir la liste des établissements ayant commis une ou
      plusieurs infractions et le nombre de contraventions connues
      testé avec **Advanced Rest Client**
      pour visualiser le resultat json : 
      GET /etablissments?etablissment="ANTIGUA"
      ou
      http://127.0.0.1:5000/etablissement?nom=antigua

      
- ### E1 (15px):
      service REST permettant à un utilisateur de se créer un profil d'utilisateur. 

- ### E2 (15px):
    Création de 2 pages : LOGIN et SignUp

    exemple de compte
    courriel: user3@courrier.uqam.ca
    mot de passe : pass

    Je n'ai pas eu le temps d'implementer l'ajout de photo et de liste d'établissements à surveiller

- ### F1 (15px)

  

