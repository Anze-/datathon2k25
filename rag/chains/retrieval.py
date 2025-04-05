class VectorRetriever:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def retrieve(self, query, k=5):
        """
        Retrieves the top-k most relevant documents from the vector store based on the query.

        Args:
            query: The query string to search for.
            k: The number of top documents to retrieve.

        Returns:
            A list of tuples containing the document ID and its similarity score.
        """
        # With score or with relevance score????
        results = self.vector_store.similarity_search_with_score(query, k=k)
        return results

    def retrieve_vector(self, vector, k=5):
        results = self.similarity_search_by_vector_with_relevance_scores(vector, k=k)
        return results

    def count_results(self, query, threshold = 0.5):
        results = self.vector_store.similarity_search(query, k=1000000)
        results = [(result, score) for result, score in results if score > threshold]
        return results

__global_retriever = None

def setup_global_retriever(vector_store):
    """
    Sets up the global retriever with the provided vector store.

    Args:
        vector_store: The vector store to be used for retrieval.
    """
    global __global_retriever
    __global_retriever = VectorRetriever(vector_store)

def get_global_retriever():
    """
    Retrieves the global retriever.

    Returns:
        The global retriever instance.
    """
    global __global_retriever
    if __global_retriever is None:
        raise ValueError("Global retriever is not set up. Call setup_global_retriever() first.")
    return __global_retriever
