from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    """
    Generates high-dimensional vector embeddings for text chunks using SentenceTransformers.

    By default, it utilizes the 'all-MiniLM-L6-v2' model, which is a lightweight,
    highly optimized model that maps sentences or paragraphs to a 384-dimensional
    dense vector space. This vector space captures the semantic meaning of the text,
    making it ideal for similarity search and retrieval in RAG pipelines.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the EmbeddingGenerator class and loads the SentenceTransformer model.

        Args:
            model_name (str): The name of the SentenceTransformer pre-trained model.
                Defaults to 'all-MiniLM-L6-v2'.
        """
        # Load the pre-trained SentenceTransformer model into memory.
        # This will download the model weights on the first run if not already cached locally.
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embedding vectors for a list of input texts.

        Args:
            texts (list[str]): A list of text strings to embed.

        Returns:
            list[list[float]]: A list of embedding vectors. Each vector is a list of floats
                with a size corresponding to the model output dimensions (384 for all-MiniLM-L6-v2).
        """
        if not texts:
            return []

        # Run the sentence transformer model to encode texts into embeddings.
        # convert_to_numpy=True creates a NumPy array, which we then convert to list format.
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        # Convert NumPy array/floats to a standard Python list of lists of floats for ChromaDB compatibility
        return embeddings.tolist()

    def generate_single_embedding(self, text: str) -> list[float]:
        """
        Generates an embedding vector for a single input text string.

        Args:
            text (str): A single text string.

        Returns:
            list[float]: A single vector representation of the text (384-dimensional float list).
        """
        if not text:
            return []

        # Generate embeddings for the list containing the single text and return the first element
        return self.generate_embeddings([text])[0]
