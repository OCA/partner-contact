Partner Revisions
=================

* Modèle de données et vues : création de la base du module ; création des
  modèles sans logique et de leurs vues ; création d’un champ fonction pour
  l’affichage des valeurs afin de pouvoir afficher les champs relation comme il
  faut (“name” de la relation au lieu de l’id.) → le champ “backend_id” devra
  être un champ de type “reference” car il peut être lié à plusieurs types de
  backend différents ;
* Logique : gestion des états des entrées du journal ; application manuelle des
  changements ; application automatique des entrées selon la configuration du
  comportement par défaut ; ne pas appliquer automatiquement de changements si
  une entrée plus récente existe (dans le cas de création d’entrée antidatée) ;
  création d’entrée “validée” lors de saisie manuelle sur les partenaires ;
  écriture de tests unitaires ;
