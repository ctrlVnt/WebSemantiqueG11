#!/usr/bin/env python3
"""
Étape 3 : Appliquer les règles OWL et comparer les résultats
"""

from rdflib import Graph, Namespace, RDF, RDFS
import owlrl
import sys
import os

# Définir les namespaces
CRIME = Namespace("http://example.org/crime/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
SCHEMA = Namespace("http://schema.org/")

def print_section(title):
    """Affiche un titre de section"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def load_data(data_file, ontology_file):
    """Charge les données et l'ontologie"""
    print_section("📂 ÉTAPE 1 : Chargement des données")
    
    g = Graph()
    
    # Charger l'ontologie
    print(f"\nChargement de l'ontologie : {ontology_file}")
    try:
        g.parse(ontology_file, format="turtle")
        print(f"✓ Ontologie chargée : {len(g)} triples")
    except Exception as e:
        print(f"❌ Erreur lors du chargement de l'ontologie : {e}")
        sys.exit(1)
    
    # Charger les données
    print(f"\nChargement des données : {data_file}")
    try:
        g.parse(data_file, format="turtle")
        print(f"✓ Données chargées : {len(g)} triples au total")
    except Exception as e:
        print(f"❌ Erreur lors du chargement des données : {e}")
        sys.exit(1)
    
    return g

def query_without_inference(g):
    """Exécute des requêtes SANS inférence"""
    print_section("🔍 ÉTAPE 2 : Requêtes SANS inférence")
    
    # Requête 1 : Compter les tueurs en série
    query1 = """
    PREFIX crime: <http://example.org/crime/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT (COUNT(?person) AS ?count)
    WHERE {
      ?person a crime:SerialKiller ;
              foaf:name ?name .
    }
    """
    
    print("\nRequête 1 : Combien de tueurs en série ?")
    result = g.query(query1)
    for row in result:
        print(f"   Résultat : {row.count} tueurs en série trouvés")
    
    # Requête 2 : Lister les criminels violents
    query2 = """
    PREFIX crime: <http://example.org/crime/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT (COUNT(?person) AS ?count)
    WHERE {
      ?person a crime:ViolentCriminal ;
              foaf:name ?name .
    }
    """
    
    print("\n Requête 2 : Combien de criminels violents ?")
    result = g.query(query2)
    for row in result:
        print(f"   Résultat : {row.count} criminels violents trouvés")
    
    # Requête 3 : Personnes avec plus de 3 victimes
    query3 = """
    PREFIX crime: <http://example.org/crime/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT ?name ?victims
    WHERE {
      ?person foaf:name ?name ;
              crime:numberOfVictims ?victims .
      FILTER(?victims >= 3)
    }
    ORDER BY DESC(?victims)
    LIMIT 5
    """
    
    print("\n📊 Requête 3 : Top 5 des personnes avec ≥3 victimes")
    result = g.query(query3)
    for row in result:
        print(f"   - {row.name} : {row.victims} victimes")

def apply_inference(g):
    """Applique le raisonneur OWL"""
    print_section("ÉTAPE 3 : Application des inférences")
    
    triples_before = len(g)
    print(f"\nNombre de triples AVANT inférence : {triples_before}")
    
    print("\nApplication du raisonneur OWL-RL...")
    try:
        owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(g)
        print("✓ Raisonneur appliqué avec succès")
    except Exception as e:
        print(f"❌ Erreur lors de l'inférence : {e}")
        return g
    
    triples_after = len(g)
    triples_inferred = triples_after - triples_before
    
    print(f"\nNombre de triples APRÈS inférence : {triples_after}")
    print(f"Nouveaux triples inférés : {triples_inferred}")
    
    if triples_inferred > 0:
        percentage = (triples_inferred / triples_before) * 100
        print(f"Augmentation : +{percentage:.1f}%")
    
    return g

def query_with_inference(g):
    """Exécute des requêtes AVEC inférence"""
    print_section("🔍 ÉTAPE 4 : Requêtes AVEC inférence")
    
    # Requête 1 : Compter les tueurs en série (maintenant inférés)
    query1 = """
    PREFIX crime: <http://example.org/crime/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT (COUNT(?person) AS ?count)
    WHERE {
      ?person a crime:SerialKiller ;
              foaf:name ?name .
    }
    """
    
    print("\n Requête 1 : Combien de tueurs en série ?")
    result = g.query(query1)
    for row in result:
        print(f"   Résultat : {row.count} tueurs en série trouvés")
    
    # Requête 2 : Lister les tueurs en série
    query2 = """
    PREFIX crime: <http://example.org/crime/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT ?name ?victims
    WHERE {
      ?person a crime:SerialKiller ;
              foaf:name ?name ;
              crime:numberOfVictims ?victims .
    }
    ORDER BY DESC(?victims)
    LIMIT 10
    """
    
    print("\n📊 Requête 2 : Top 10 tueurs en série (inférés)")
    result = g.query(query2)
    for i, row in enumerate(result, 1):
        print(f"   {i}. {row.name} : {row.victims} victimes")
    
    # Requête 3 : Criminels violents
    query3 = """
    PREFIX crime: <http://example.org/crime/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    
    SELECT (COUNT(?person) AS ?count)
    WHERE {
      ?person a crime:ViolentCriminal .
    }
    """
    
    print("\n📊 Requête 3 : Combien de criminels violents ?")
    result = g.query(query3)
    for row in result:
        print(f"   Résultat : {row.count} criminels violents trouvés")
    
    

def save_results(g, output_file):
    """Sauvegarde les résultats avec inférences"""
    print_section("ÉTAPE 6 : Sauvegarde des résultats")
    
    print(f"\nSauvegarde dans : {output_file}")
    try:
        g.serialize(output_file, format="turtle")
        file_size = os.path.getsize(output_file) / 1024  # en KB
        print(f"✓ Fichier sauvegardé : {file_size:.1f} KB")
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")

def main():
    """Fonction principale"""
    
    
    # Chemins des fichiers
    DATA_FILE = "data/profile_killers.ttl"
    ONTOLOGY_FILE = "ontology/crime_ontology.ttl"
    OUTPUT_FILE = "data/profile_killers_inferred.ttl"
    
    # Vérifier que les fichiers existent
    if not os.path.exists(DATA_FILE):
        print(f"❌ Fichier non trouvé : {DATA_FILE}")
        print("Assurez-vous que votre fichier TTL est dans le dossier 'data/'")
        sys.exit(1)
    
    if not os.path.exists(ONTOLOGY_FILE):
        print(f"❌ Fichier non trouvé : {ONTOLOGY_FILE}")
        print("Assurez-vous que l'ontologie est dans le dossier 'ontology/'")
        sys.exit(1)
    
    # Étape 1 : Charger les données
    g = load_data(DATA_FILE, ONTOLOGY_FILE)
    
    # Étape 2 : Requêtes SANS inférence
    query_without_inference(g)
    
    # Étape 3 : Appliquer les inférences
    g_inferred = apply_inference(g)
    
    # Étape 4 : Requêtes AVEC inférence
    query_with_inference(g_inferred)
    
    # Étape 5: Sauvegarder
    save_results(g_inferred, OUTPUT_FILE)
    
if __name__ == "__main__":
    main()