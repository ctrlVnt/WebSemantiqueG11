"""
Générateur de description VOID simplifié
Étape 5 : Créer la description VOID de killers.ttl
"""


from rdflib import Graph, Namespace, Literal, URIRef, RDF, RDFS
from rdflib.namespace import FOAF, DCTERMS, XSD, OWL
from collections import Counter
from datetime import datetime
import sys
import os

# Namespaces
VOID = Namespace("http://rdfs.org/ns/void#")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
CRIME = Namespace("http://example.org/crime/")
SCHEMA = Namespace("http://schema.org/")



def create_void_description(data_file, output_file):
    """Crée une description VOID pour le dataset"""
      
    # Charger les données
    g = Graph()
    try:
        g.parse(data_file, format="turtle")
        print(f"✓ Données chargées : {len(g)} triples")
    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)
    
    # Créer le graphe VOID
    void_g = Graph()
    void_g.bind("void", VOID)
    void_g.bind("dcat", DCAT)
    void_g.bind("dcterms", DCTERMS)
    void_g.bind("foaf", FOAF)
    void_g.bind("crime", CRIME)
    void_g.bind("owl", OWL)
    
    dataset_uri = CRIME.dataset
    
    print("Calcul des statistiques")
    
    # Type
    void_g.add((dataset_uri, RDF.type, VOID.Dataset))
    void_g.add((dataset_uri, RDF.type, DCAT.Dataset))
    
    # Métadonnées de base
    void_g.add((dataset_uri, DCTERMS.title, 
               Literal("Serial Killers Dataset", lang="en")))
    void_g.add((dataset_uri, DCTERMS.title, 
               Literal("Base de données des tueurs en série", lang="fr")))
    void_g.add((dataset_uri, DCTERMS.description, 
               Literal("A comprehensive RDF dataset about serial killers", lang="en")))
    
    # Dates
    today = datetime.now().strftime("%Y-%m-%d")
    void_g.add((dataset_uri, DCTERMS.created, Literal(today, datatype=XSD.date)))
    void_g.add((dataset_uri, DCTERMS.modified, Literal(today, datatype=XSD.date)))
    
    # Licence
    void_g.add((dataset_uri, DCTERMS.license, 
               URIRef("http://creativecommons.org/licenses/by/4.0/")))
    
    # URI Space
    void_g.add((dataset_uri, VOID.uriSpace, Literal("http://example.org/crime/")))
    
    # Statistiques de base
    num_triples = len(g)
    void_g.add((dataset_uri, VOID.triples, Literal(num_triples)))
    print(f"  • Triples : {num_triples}")
    
    # Sujets distincts
    subjects = set(g.subjects())
    void_g.add((dataset_uri, VOID.distinctSubjects, Literal(len(subjects))))
    print(f"  • Sujets distincts : {len(subjects)}")
    
    # Objets distincts
    objects = set(g.objects())
    void_g.add((dataset_uri, VOID.distinctObjects, Literal(len(objects))))
    print(f"  • Objets distincts : {len(objects)}")
    
    # Entités (ressources avec type)
    entities = set(g.subjects(RDF.type, None))
    void_g.add((dataset_uri, VOID.entities, Literal(len(entities))))
    print(f"  • Entités : {len(entities)}")
    
    # Propriétés
    properties = set(g.predicates())
    void_g.add((dataset_uri, VOID.properties, Literal(len(properties))))
    print(f"  • Propriétés : {len(properties)}")
    
    # Classes
    classes = set(g.objects(None, RDF.type))
    void_g.add((dataset_uri, VOID.classes, Literal(len(classes))))
    print(f"  • Classes : {len(classes)}")
    
    print("Distribution des classes")
    
    # Compter les instances par classe
    class_counts = Counter()
    for s in g.subjects(RDF.type, None):
        for o in g.objects(s, RDF.type):
            class_counts[o] += 1
    
    # Top 5 classes
    print("\n  Top 5 classes :")
    for cls, count in class_counts.most_common(5):
        class_name = str(cls).split('/')[-1].split('#')[-1]
        print(f"    • {class_name} : {count} instances")
        
        # Ajouter au VOID
        partition = URIRef(f"{dataset_uri}-partition-{hash(cls)}")
        void_g.add((dataset_uri, VOID.classPartition, partition))
        void_g.add((partition, VOID['class'], cls))
        void_g.add((partition, VOID.entities, Literal(count)))
    
    print("Recherche des liens externes")
    
    # Chercher les liens owl:sameAs
    external_links = {
        'dbpedia': 0,
        'wikidata': 0,
        'geonames': 0
    }
    
    for s, p, o in g.triples((None, OWL.sameAs, None)):
        if isinstance(o, URIRef):
            if 'dbpedia.org' in str(o):
                external_links['dbpedia'] += 1
            elif 'wikidata.org' in str(o):
                external_links['wikidata'] += 1
            elif 'geonames.org' in str(o):
                external_links['geonames'] += 1
    
    print("\n  Liens trouvés :")
    for name, count in external_links.items():
        if count > 0:
            print(f"    • {name.capitalize()} : {count} liens")
    
    # Ajouter les linksets au VOID
    if external_links['dbpedia'] > 0:
        linkset = URIRef(f"{dataset_uri}-linkset-dbpedia")
        void_g.add((linkset, RDF.type, VOID.Linkset))
        void_g.add((linkset, VOID.linkPredicate, OWL.sameAs))
        void_g.add((linkset, VOID.subjectsTarget, dataset_uri))
        void_g.add((linkset, VOID.objectsTarget, URIRef("http://dbpedia.org/")))
        void_g.add((linkset, VOID.triples, Literal(external_links['dbpedia'])))
    
    if external_links['wikidata'] > 0:
        linkset = URIRef(f"{dataset_uri}-linkset-wikidata")
        void_g.add((linkset, RDF.type, VOID.Linkset))
        void_g.add((linkset, VOID.linkPredicate, OWL.sameAs))
        void_g.add((linkset, VOID.subjectsTarget, dataset_uri))
        void_g.add((linkset, VOID.objectsTarget, URIRef("http://www.wikidata.org/")))
        void_g.add((linkset, VOID.triples, Literal(external_links['wikidata'])))
    
    print("Vocabulaires détectés")
    
    # Détecter les vocabulaires utilisés
    vocabularies = set()
    for p in properties:
        ns = str(p).rsplit('/', 1)[0] + '/' if '/' in str(p) else str(p).rsplit('#', 1)[0] + '#'
        vocabularies.add(ns)
    
    print(f"\n  {len(vocabularies)} vocabulaires détectés :")
    for vocab in sorted(vocabularies)[:10]:
        print(f"    • {vocab}")
        void_g.add((dataset_uri, VOID.vocabulary, URIRef(vocab)))
    
    print("Sauvegarde de la description VOID")
    
    # Sauvegarder
    try:
        void_g.serialize(output_file, format="turtle")
        file_size = os.path.getsize(output_file) / 1024
        print(f"\n✓ Fichier sauvegardé : {output_file}")
        print(f"  Taille : {file_size:.1f} KB")
        print(f"  Triples VOID : {len(void_g)}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")
    

def main():
    """Fonction principale"""
    
    # Chemins
    DATA_FILE = "data/profile_killers_inferred.ttl"
    OUTPUT_FILE = "void/void_description.ttl"
    
    # Vérifier que le fichier existe
    if not os.path.exists(DATA_FILE):
        print(f"❌ Fichier non trouvé : {DATA_FILE}")
        print("\nAssurez-vous d'avoir exécuté le script d'inférence avant !")
        print("Commande : python scripts/inference.py")
        sys.exit(1)
    
    # Créer le dossier void s'il n'existe pas
    os.makedirs("void", exist_ok=True)
    
    # Générer la description VOID
    create_void_description(DATA_FILE, OUTPUT_FILE)

if __name__ == "__main__":
    main()