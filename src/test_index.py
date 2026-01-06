from index_builder import MultiSourceIndex
from contradiction_detection import ContradictionDetector
from log_utils import RAGLogger

# Build the index
index = MultiSourceIndex()
index.build("data")

query = [
    "How long is version history kept on the Basic plan?",
    "What are the API rate limits for Basic and Pro users?",
    "How often does Nimbus sync notes on desktop vs mobile?",
    "Can I use Nimbus offline? What features are available?",
    "Does Nimbus support team collaboration workflows?",
    "How do I connect Nimbus to third-party integrations like Slack or Google Drive?",
    "What should I do if my device stops syncing and shows a red error icon?",
    "Which plan keeps the longest version history and for how long?",
    "How many members can be in a Nimbus team before performance issues occur?",
    "Does Nimbus automatically retry failed sync operations?"
    
]



# ---------- RETRIEVE + RERANK ----------
for i in query:
        retrieved = index.retrieve(i, top_k=5)
        reranked = index.rerank(i, retrieved, top_k=3)

        print("\n=== Final Reranked Results ===\n")
        for chunk, score in reranked:
            print("SOURCE:", chunk.source_type)
            print("RERANK SCORE:", round(score, 3))
            print(chunk.text[:200], "...")
            print("-" * 50)

        # ---------- CONTRADICTION DETECTION ----------
        detector = ContradictionDetector(model="qwen2.5-vl-7b")   # <-- MAKE SURE THIS MATCHES LM STUDIO
        analysis = detector.analyze(i, reranked)

        print("\n=== CONTRADICTION ANALYSIS ===\n")
        print("Status:", analysis["status"])
        print("Explanation:", analysis["explanation"])
        print("\nAuthoritative Answer:")
        print(analysis["authoritative_answer"])

        logger = RAGLogger()
        logger.log(i, retrieved, reranked, analysis)
