from neo4j import GraphDatabase


class Neo4jMerger:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def merge_nodes(self):
        with self.driver.session() as session:
            session.write_transaction(self._merge_ventilation_nodes)

    @staticmethod
    def _merge_ventilation_nodes(tx):
        query = """
        // Match nodes to be merged
        MATCH (a:Attribute {name: '通风率'}), (e:__Entity__ {name: '卷烟总通风率'})

        // Merge both nodes into a new node '卷烟通风率'
        MERGE (v:卷烟通风率 {name: '卷烟通风率'})

        // Set properties from both nodes
        SET v += a, v += e

        // Delete old nodes after merging properties
        DELETE a, e

        // Return the newly created node
        RETURN v
        """
        result = tx.run(query)
        for record in result:
            print(f"Merged node: {record['v']}")


if __name__ == "__main__":
    # Neo4j connection details
    uri = "neo4j+s://bf17663e.databases.neo4j.io"
    user = "neo4j"
    password = "aRd5bEfCEY7w097XJQz8PB4nWT3CTkpsnWiOLeXYCUk"

    # Initialize Neo4jMerger
    merger = Neo4jMerger(uri, user, password)

    # Execute the merge operation
    try:
        merger.merge_nodes()
    finally:
        merger.close()
