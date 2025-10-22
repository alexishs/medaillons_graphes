import random
from metier import utils
from metier.bronze import traitement_bronze
from metier.silver import traitement_silver

utils.definir_en_test()

def generer_csv()-> None:
    
    liste_entiers = list(range(1,1000000))
    with open(utils.chemin_base(f"{utils.REPERTOIRE_DONNEES_BRUTES}/noeuds.csv"), mode='w', encoding='utf-8') as fichier:
        for numero in liste_entiers:
            fichier.write(f"{numero},Personne,Nom_{numero}\n")
    random.shuffle(liste_entiers)
    with open(utils.chemin_base(f"{utils.REPERTOIRE_DONNEES_BRUTES}/relations.csv"), mode='w', encoding='utf-8') as fichier:
        numero_precedent = 0
        for numero in liste_entiers:
            if numero_precedent > 0:
                fichier.write(f"{numero_precedent},{numero},REL\n")
                numero_precedent = 0
            else:
                numero_precedent = numero

utils.creer_repertoires()
generer_csv()
traitement_bronze()
traitement_silver()