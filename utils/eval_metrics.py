#============================= 简单RAG评测指标 =============================#
def calculate_recall(retrieved: list[str], relevant: list[str]) -> float:
    hit = sum(1 for d in retrieved if d in relevant)
    return hit / len(relevant) if relevant else 0.0

def evaluate_rag(query: str, answer: str, docs: list[str]) -> dict:
    return {
        "query": query,
        "answer_length": len(answer),
        "retrieved_count": len(docs),
        "score": len(answer) > 0
    }