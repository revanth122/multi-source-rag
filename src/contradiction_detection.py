import json
import re
from openai import OpenAI

# Connect to LM Studio local server
client = OpenAI(
    base_url="http://localhost:1234/v1",   # LM Studio server endpoint
    api_key="lm-studio"                    # dummy key required by SDK
)


class ContradictionDetector:

    def __init__(self, model="qwen2.5-vl-7b"):
        """
        IMPORTANT:
        The model name must match EXACTLY what LM Studio shows
        in the 'Server' tab when the model is loaded.
        Example values:
            "qwen2.5-vl-7b"
            "qwen/qwen2.5-vl-7b"
        """
        self.model = model

    def analyze(self, query, chunks):
        """
        Uses a local LLM to compare retrieved chunks and detect contradictions.
        Always returns a JSON object.
        """

        # Combine chunk texts for the LLM
        evidence = "\n\n".join([
            f"[SOURCE: {c.source_type}] {c.text}"
            for c, _score in chunks
        ])

        # Strict JSON-only instruction
        prompt = f"""
You are an AI system that MUST output ONLY valid JSON.

USER QUESTION:
\"\"\"{query}\"\"\"

EVIDENCE FROM DIFFERENT SOURCES:
---
{evidence}
---

INSTRUCTIONS (FOLLOW EXACTLY):
1. Compare all evidence and determine if sources AGREE or CONTRADICT.
2. Authority ranking:
   - docs (highest)
   - blogs
   - forums (lowest)
3. Produce ONLY valid JSON with this exact structure:

{{
  "status": "consistent" | "contradiction" | "insufficient_data",
  "explanation": "Short explanation of agreement or contradiction.",
  "authoritative_answer": "Final answer using highest-authority source."
}}

4. DO NOT output anything outside the JSON.
5. DO NOT add comments, markdown, or extra explanations.
6. If unsure, use "insufficient_data".
"""

        # Query LM Studio local model
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",
                     "content": "You analyze contradictions across RAG evidence and respond ONLY in JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )
        except Exception as e:
            return {
                "status": "insufficient_data",
                "explanation": f"Model error: {str(e)}",
                "authoritative_answer": ""
            }

        raw = response.choices[0].message.content.strip()

        # Extract JSON even if the model adds extra text
        json_match = re.search(r"\{.*\}", raw, re.DOTALL)
        if json_match:
            try:
                cleaned = json_match.group()
                return json.loads(cleaned)
            except Exception:
                pass

        # Final fallback
        return {
            "status": "insufficient_data",
            "explanation": "Model returned invalid JSON.",
            "authoritative_answer": ""
        }
