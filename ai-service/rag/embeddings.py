import chromadb.utils.embedding_functions as ef

def get_embedding_function(model_name: str = "all-MiniLM-L6-v2"):
    """
    Returns ChromaDB's default local embedding function using the 'all-MiniLM-L6-v2' model.
    Runs locally using ONNX runtime without external API keys.
    """
    return ef.DefaultEmbeddingFunction()
