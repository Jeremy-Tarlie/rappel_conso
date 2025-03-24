# RappelConso - Application de Consultation des Rappels de Produits

## Description
Cette application Python permet de consulter la base de données RappelConso, qui répertorie les rappels de produits en France. Elle offre une interface en ligne de commande permettant de rechercher des produits selon différents critères et d'afficher les informations détaillées sur les rappels.

## Fonctionnalités
- Recherche multicritères (libellé, marque, catégorie, distributeur, risque)
- Affichage détaillé des résultats
- Gestion robuste des erreurs
- Interface utilisateur interactive

## Prérequis
- Python 3.6 ou supérieur
- Modules requis :
  - `requests`
  - `json`

## Installation

Clonez le dépôt :

```bash
git clone https://github.com/Jeremy-Tarlie/rappel_conso.git
cd rappelconso
```

Installez les dépendances :

Si vous avez un fichier requirements.txt, vous pouvez installer toutes les dépendances nécessaires d'un coup avec la commande suivante :

```bash
pip install -r requirements.txt
```
## Utilisation
Lancez le script :

```bash
python main.py
```