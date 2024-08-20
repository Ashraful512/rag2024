from neo4j import GraphDatabase

class Neo4jMerger:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def merge_nodes(self):
        with self.driver.session() as session:
            # Ensure the target node exists
            session.execute_write(self._create_target_node)
            # Merge nodes with the same meaning or duplicate nodes into '卷烟通风率'
            session.execute_write(self._merge_same_meaning_nodes)

    @staticmethod
    def _create_target_node(tx):
        query = """
        MERGE (target:__Entity__ {name: "卷烟通风率"})
        """
        tx.run(query)

    def _merge_same_meaning_nodes(self, tx):
        # Define the same meaning nodes to be merged
        same_meaning_nodes = [
            "通风率",
            "卷烟纸透气度",
            "滤嘴通风率",
            "卷烟总通风率"
        ]

        # For each node to be merged
        for node_name in same_meaning_nodes:
            # Retrieve all relationships of the node
            result = tx.run(f"""
                MATCH (n:__Entity__ {{name: "{node_name}"}})
                RETURN n
            """)
            record = result.single()
            if record is None:
                continue

            # Get properties of the node
            node_properties = record["n"].items()

            # Create the Cypher query to merge properties
            set_clauses = []
            for key, value in node_properties:
                if key != "name":  # Avoid overwriting the 'name' property
                    set_clauses.append(f'SET target.{key} = coalesce(target.{key}, {repr(value)})')

            set_query = "\n".join(set_clauses)

            # Transfer outgoing relationships by iterating through relationship types
            outgoing_rels = tx.run(f"""
                MATCH (n:__Entity__ {{name: "{node_name}"}})-[r]->(m)
                RETURN type(r) AS rel_type, properties(r) AS rel_props, m.element_id AS m_element_id
            """)
            for rel in outgoing_rels:
                rel_type = rel["rel_type"]
                rel_props = rel["rel_props"]
                target_node_id = rel["m_element_id"]

                # Generate the SET clauses for each property in rel_props
                set_rel_clauses = [f"SET newRel.{key} = {repr(value)}" for key, value in rel_props.items()]
                set_rel_query = "\n".join(set_rel_clauses)

                # Generate the MERGE clause for each relationship type
                query = f"""
                MATCH (target:__Entity__ {{name: "卷烟通风率"}}), (m)
                WHERE m.element_id = "{target_node_id}"
                MERGE (target)-[newRel:`{rel_type}`]->(m)
                {set_rel_query}
                """
                tx.run(query)

            # Transfer incoming relationships similarly
            incoming_rels = tx.run(f"""
                MATCH (m)-[r]->(n:__Entity__ {{name: "{node_name}"}})
                RETURN type(r) AS rel_type, properties(r) AS rel_props, m.element_id AS m_element_id
            """)
            for rel in incoming_rels:
                rel_type = rel["rel_type"]
                rel_props = rel["rel_props"]
                source_node_id = rel["m_element_id"]

                # Generate the SET clauses for each property in rel_props
                set_rel_clauses = [f"SET newRel.{key} = {repr(value)}" for key, value in rel_props.items()]
                set_rel_query = "\n".join(set_rel_clauses)

                query = f"""
                MATCH (target:__Entity__ {{name: "卷烟通风率"}}), (m)
                WHERE m.element_id = "{source_node_id}"
                MERGE (m)-[newRel:`{rel_type}`]->(target)
                {set_rel_query}
                """
                tx.run(query)

            # Delete the old node
            query = f"""
            MATCH (n:__Entity__ {{name: "{node_name}"}})
            DETACH DELETE n
            """
            tx.run(query)

if __name__ == "__main__":
    # Set your connection details here
    uri = "neo4j+s://bf17663e.databases.neo4j.io"
    user = "neo4j"
    password = "aRd5bEfCEY7w097XJQz8PB4nWT3CTkpsnWiOLeXYCUk"

    # Instantiate the merger and perform the merge
    merger = Neo4jMerger(uri, user, password)
    try:
        merger.merge_nodes()
        print("Merge completed successfully.")
    finally:
        merger.close()
