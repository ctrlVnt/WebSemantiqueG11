# Killer Dataset

Killer dataset for Web Semantic project

## Files

* *profile_killers.csv*: dataset file downloaded [here](https://www.kaggle.com/datasets/dante890b/wikipedia-serial-killers-list)
* *killers.ttl*: Dataset in Turtle RDF format
* *query.sparql*: SPARQL CONSTRUCT to transform CSV in RDF
* *nos_equetes.sparql*: some SPARQL requests

## How to use in Apache Fuseki

### ⚙️ Install Apache Fuseki

1. Go to [https://jena.apache.org/download/](https://jena.apache.org/download/)
2. Download **Apache Jena Fuseki** (`apache-jena-fuseki-x.x.x.zip`)
3. Extract it to a folder, for example:
   - Windows: `C:\fuseki\`
   - macOS/Linux: `~/fuseki/`

### ⚙️ Start the Fuseki Server

Open a terminal (or command prompt) and navigate to the Fuseki folder.  
Then run the following command:

**On macOS / Linux:**
```bash
cd ~/fuseki
./fuseki-server
```

**On Windows:**
```bash
cd C:\fuseki
fuseki-server.bat
```

By default, Fuseki will start on port 3030

### 🌐 Access the Web Interface

Once the server is running, open your browser and go to:

👉 http://localhost:3030

You should see the Apache Jena Fuseki dashboard, where you can:

* Create new datasets
* Upload RDF files (.ttl, .rdf, .nt, etc.)
* Run SPARQL queries
* Manage data via the web UI