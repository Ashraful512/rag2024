RAG2024: Graph-Based Knowledge Retrieval System
Overview
RAG2024 is a project that leverages GraphRAG, a graph-based knowledge retrieval system, for extracting nodes and relationships from text data using a Large Language Model (LLM). The resulting graph is visualized and managed in a Neo4j graph database. This project aims to enhance data processing by converting various data formats (e.g., PDF) into usable text files, indexing them, and visualizing relationships within a graph database.

Project Structure
convert_pdf_to_txt.py: Converts PDF files into .txt format, which is required for GraphRAG to process the data.
graphrag_importer.py: Imports extracted data from .parquet files into Neo4j to generate the graph structure.
nodes_merger.py: Merges duplicate nodes or nodes with similar meanings into a single unified node in Neo4j.
Installation

Clone the repository:

git clone https://github.com/Ashraful512/rag2024.git
cd rag2024
Set up the Python environment:
Make sure you have Python 3.10+ installed. You can create a virtual environment using the following command:

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required libraries:


pip install -r requirements.txt
Install Neo4j and configure it:

Usage
1. Converting PDFs to Text
Before running GraphRAG, convert your PDF files to text using the provided script:

python convert_pdf_to_txt.py
2. Initializing GraphRAG Indexing
Once your text data is ready, initialize the GraphRAG indexing by running the following command:

python -m graphrag.index --init --root ./ragtest
This will generate a YAML configuration file and prompt documents that can be adjusted as necessary. 
in settings.YAML you will have to insert LLM and Embeddings API key's information

3. Running GraphRAG to Extract Nodes and Relationships
After configuring the YAML and prompt documents, run the indexing again to extract nodes and relationships:

python -m graphrag.index --root ./ragtest
This process will output/artifacts folder .parquet files containing the extracted data.

4. Importing Data into Neo4j
set up your Neo4j credentials:
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password

To import the extracted data into Neo4j, use the graphrag_importer.py script:

python graphrag_importer.py 
This will create a graph in Neo4j using the data from the .parquet files.

5. Merging Duplicate or Similar Nodes
After visualizing the graph in Neo4j, you may notice duplicate or similarly-meaning nodes. Use the nodes_merger.py script to merge these nodes:

python nodes_merger.py 
The script will automatically merge nodes with names like "通风率", "卷烟纸透气度", "滤嘴通风率", and "卷烟总通风率" into a single node labeled "卷烟通风率".

How It Works
Node Merging Overview
Neo4j Connection Setup:
The Neo4jMerger class initializes a connection to the Neo4j database using the provided URI, username, and password.

Merging Nodes:
The script ensures that a target node exists for merging (e.g., "卷烟通风率") and identifies nodes with similar names to merge their properties and relationships into the target node.

Handling Properties and Relationships:
For each duplicate node, its properties and relationships are transferred to the target node using Cypher SET and MERGE commands.

Cleaning Up:
After the properties and relationships are transferred, the duplicate nodes are deleted from the graph.
