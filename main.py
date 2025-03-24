import requests
import json
import sys
import time

def verifier_api():
    try:
        test_url = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso0/records"
        response = requests.get(test_url, timeout=5)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def afficher_menu():
    while True:
        try:
            print("\nChoisissez votre critère de recherche :")
            print("1. Libellé du produit")
            print("2. Marque")
            print("3. Catégorie de produit")
            print("4. Distributeur")
            print("5. Risque")
            print("0. Quitter")
            
            choix = input("Votre choix (0-5) : ")
            
            if choix not in ["0", "1", "2", "3", "4", "5"]:
                raise ValueError("Choix invalide")
                
            return choix
            
        except ValueError as e:
            print(f"\nErreur : {e}")
            print("Veuillez entrer un nombre entre 0 et 5")
            time.sleep(1)

def construire_requete(choix):
    filtres = {
        "1": ("libelle", "Entrez le libellé du produit recherché : "),
        "2": ("nom_de_la_marque_du_produit", "Entrez le nom de la marque : "),
        "3": ("categorie_de_produit", "Entrez la catégorie de produit : "),
        "4": ("distributeurs", "Entrez le nom du distributeur : "),
        "5": ("risques_encourus_par_le_consommateur", "Entrez le type de risque : ")
    }

    if choix == "0":
        sys.exit("Au revoir !")

    if choix not in filtres:
        raise RappelConsoError("Choix de filtre invalide")

    champ, message = filtres[choix]
    valeur = input(message).strip()
    
    if not valeur:
        raise RappelConsoError("La valeur de recherche ne peut pas être vide")
        
    return champ, valeur

def effectuer_requete(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        raise RappelConsoError("Le serveur met trop de temps à répondre")
    except requests.exceptions.HTTPError as e:
        raise RappelConsoError(f"Erreur HTTP : {e.response.status_code}")
    except requests.exceptions.RequestException as e:
        raise RappelConsoError(f"Erreur lors de la requête : {str(e)}")
    except json.JSONDecodeError:
        raise RappelConsoError("Erreur : Réponse du serveur invalide")

def afficher_resultats(data):
    total = data.get('total_count', 0)
    
    if total == 0:
        print("\nAucun résultat trouvé")
        return
        
    print(f"\nNombre total de résultats : {total}\n")

    for item in data.get('results', []):
        try:
            print("=" * 50)
            print(f"Produit: {item.get('libelle', 'Non spécifié')}")
            print(f"Marque: {item.get('nom_de_la_marque_du_produit', 'Non spécifiée')}")
            print(f"Sous-catégorie: {item.get('categorie_de_produit', 'Non spécifiée')}")
            print(f"Motif du rappel: {item.get('motif_du_rappel', 'Non spécifié')}")
            print(f"Date de publication: {item.get('date_de_publication', 'Non spécifiée')}")
            print(f"Distributeurs: {item.get('distributeurs', 'Non spécifiés')}")
            print(f"Risques: {item.get('risques_encourus_par_le_consommateur', 'Non spécifiés')}")
            print("=" * 50)
            print()
        except Exception as e:
            print(f"Erreur lors de l'affichage d'un résultat : {str(e)}")
            continue

def main():
    print("Bienvenue dans l'application RappelConso")
    
    if not verifier_connexion_internet():
        print("Erreur : Impossible de se connecter à l'API. Vérifiez votre connexion internet.")
        return

    while True:
        try:
            choix = afficher_menu()
            
            champ, valeur = construire_requete(choix)
            
            url = f"https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso0/records?where={champ}%20LIKE%20%27%25{valeur}%25%27"
            
            data = effectuer_requete(url)
            
            afficher_resultats(data)
            
            continuer = input("\nVoulez-vous faire une autre recherche ? (o/n) : ").lower()
            if continuer != 'o':
                print("Au revoir !")
                break
                
        except RappelConsoError as e:
            print(f"\nErreur : {str(e)}")
            time.sleep(2)
        except KeyboardInterrupt:
            print("\nOpération annulée par l'utilisateur")
            break
        except Exception as e:
            print(f"\nUne erreur inattendue s'est produite : {str(e)}")
            time.sleep(2)

main()