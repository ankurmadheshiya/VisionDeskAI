import os
import chromadb

class ChromaDBManager:
    """
    Manages similarity search operations using ChromaDB.

    This class encapsulates a persistent ChromaDB client, allowing document
    embeddings and their corresponding texts and metadatas to be stored on disk.
    It also provides an interface to query stored documents using vector similarity.
    """

    def __init__(self, db_path: str = None):
        """
        Initializes the ChromaDB persistent client.

        Args:
            db_path (str, optional): The directory where ChromaDB stores its data.
                Defaults to a directory named 'chroma_db' inside 'module2' directory.
        """
        if db_path is None:
            # Get the path of the current module2 folder and create a chroma_db directory inside it
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "chroma_db")

        # Create the directory if it doesn't already exist
        os.makedirs(db_path, exist_ok=True)

        # Initialize the persistent client. ChromaDB will save files in the specified path.
        self.client = chromadb.PersistentClient(path=db_path)

    def get_or_create_collection(self, collection_name: str):
        """
        Retrieves an existing ChromaDB collection or creates a new one.

        Args:
            collection_name (str): The unique name of the collection.

        Returns:
            chromadb.Collection: The collection object.
        """
        # Returns the collection or creates it if it does not exist yet.
        return self.client.get_or_create_collection(name=collection_name)

    def add_documents(
        self,
        collection_name: str,
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
        ids: list[str]
    ) -> None:
        """
        Stores document chunks, embeddings, and metadatas into the specified collection.

        Args:
            collection_name (str): The name of the target collection.
            documents (list[str]): The plain-text contents of the chunks.
            embeddings (list[list[float]]): The dense vector representations of the chunks.
            metadatas (list[dict]): A list of dictionaries containing metadata (e.g. page numbers).
            ids (list[str]): A list of unique strings to identify each document chunk.
        """
        # Retrieve the collection
        collection = self.get_or_create_collection(collection_name)

        # Add the data to ChromaDB. Passing embeddings explicitly overrides ChromaDB's
        # default local embedding behavior and uses our precomputed sentence-transformer embeddings.
        collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def query_similarity(self, collection_name: str, query_embedding: list[float], n_results: int = 3) -> list[dict]:
        """
        Performs a vector similarity search to find the closest chunks for a query.

        Args:
            collection_name (str): The name of the collection to query.
            query_embedding (list[float]): The 384-dimensional query embedding vector.
            n_results (int): The maximum number of nearest neighbor chunks to return (default is 3).

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a matched chunk
                and contains "text", "metadata", "id", and "distance".
        """
        # Retrieve the collection
        collection = self.get_or_create_collection(collection_name)

        # Query the collection. We pass the query embedding vector and get n nearest neighbors.
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        formatted_results = []
        
        # Parse the ChromaDB dictionary results and build a user-friendly list of dictionaries
        if results and "documents" in results and results["documents"]:
            # Extracted arrays (each is a list containing list elements for our single query)
            docs = results["documents"][0]
            metas = results["metadatas"][0] if results["metadatas"] else [None] * len(docs)
            ids = results["ids"][0]
            distances = results["distances"][0] if results["distances"] else [0.0] * len(docs)

            for i in range(len(docs)):
                formatted_results.append({
                    "id": ids[i],
                    "text": docs[i],
                    "metadata": metas[i],
                    "distance": distances[i]
                })

        return formatted_results

    def delete_collection(self, collection_name: str) -> None:
        """
        Deletes a collection and all of its items from the database.

        Args:
            collection_name (str): The name of the collection to delete.
        """
        try:
            self.client.delete_collection(name=collection_name)
        except Exception:
            # Collection may not exist, suppress error to prevent crashes during pipeline resets
            pass
