import os
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import CrossEncoder


# Import your chunking functions
from chunking import load_files


class MultiSourceIndex:
    """
    Builds a vector index containing chunks from:
    - docs
    - forums
    - blogs

    Also supports weighted retrieval.
    """

    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.chunks = []
        self.embeddings = None
        self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
        
    def rerank(self, query, retrieved_chunks, top_k=3):
        """
        Reranks retrieved chunks using a cross-encoder model.
        """
        # Prepare pairs for scoring
        pairs = [(query, chunk.text) for chunk, _ in retrieved_chunks]

        # Get scores from cross-encoder
        scores = self.reranker.predict(pairs)

        # Combine chunks with rerank scores
        reranked = list(zip(retrieved_chunks, scores))

        # Sort by cross-encoder score (higher = more relevant)
        reranked.sort(key=lambda x: x[1], reverse=True)

        # Extract only the chunks with new scores
        final = [(item[0][0], float(item[1])) for item in reranked[:top_k]]

        return final



    def build(self, base_path):
      print("BASE PATH:", base_path)

      print("Loading documentation chunks...")
      doc_chunks = load_files(base_path, "docs")
      print("Loaded doc chunks:", len(doc_chunks))

      print("Loading forum chunks...")
      forum_chunks = load_files(base_path, "forums")
      print("Loaded forum chunks:", len(forum_chunks))

      print("Loading blog chunks...")
      blog_chunks = load_files(base_path, "blogs")
      print("Loaded blog chunks:", len(blog_chunks))

      self.chunks = doc_chunks + forum_chunks + blog_chunks
      print("Total chunks loaded:", len(self.chunks))

      texts = [chunk.text for chunk in self.chunks]
      print("Number of texts:", len(texts))

      print("Building embeddings...")
      self.embeddings = self.model.encode(texts, convert_to_numpy=True)

      print("Index build complete.")


    def retrieve(self, query, source_weights=None, top_k=5):
        """
        Retrieves top-k chunks using weighted cosine similarity.

        source_weights: dict like {"docs": 1.2, "blogs": 1.0, "forums": 0.8}
        """

        if self.embeddings is None:
            raise ValueError("Index has not been built yet.")

        # Default weights
        if source_weights is None:
            source_weights = {"docs": 1.2, "blogs": 1.0, "forums": 0.9}

        # Embed the query
        q_emb = self.model.encode([query], convert_to_numpy=True)

        # Compute similarity
        sims = cosine_similarity(q_emb, self.embeddings)[0]

        # Apply weights
        weighted_scores = []
        for i, chunk in enumerate(self.chunks):
            weight = source_weights.get(chunk.source_type, 1.0)
            weighted_scores.append((i, sims[i] * weight))

        # Sort by similarity score
        weighted_scores.sort(key=lambda x: x[1], reverse=True)

        # Return top results
        results = []
        for idx, score in weighted_scores[:top_k]:
            results.append((self.chunks[idx], score))

        return results
