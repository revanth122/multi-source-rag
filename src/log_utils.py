import json
import datetime

class RAGLogger:

    def __init__(self, log_path="rag_logs.jsonl"):
        """
        Logs each query as a JSON line into rag_logs.jsonl
        """
        self.log_path = log_path

    def log(self, query, retrieved, reranked, contradiction):
        """
        Writes one log entry containing:
        - raw retrieved results
        - reranked results
        - contradiction analysis
        """

        entry = {
            "timestamp": datetime.datetime.now().isoformat(),

            "query": query,

            "retrieved": [
                {
                    "source": chunk.source_type,
                    "retrieval_score": float(score),
                    "preview": chunk.text[:150]
                }
                for chunk, score in retrieved
            ],

            "reranked": [
                {
                    "source": chunk.source_type,
                    "rerank_score": float(score),
                    "preview": chunk.text[:150]
                }
                for chunk, score in reranked
            ],

            "contradiction": contradiction
        }

        # Append JSON line
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
