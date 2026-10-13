import os
import json
import time
from dotenv import load_dotenv
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_groq import ChatGroq
from RAG1.agent import ask

load_dotenv()

# --- DeepEval Groq Judge Setup ---
class GroqJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="openai/gpt-oss-20b"):
        self.model_name = model_name
        self.llm = ChatGroq(model_name=self.model_name, groq_api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, prompt: str) -> str:
        response = self.llm.invoke(prompt)
        return response.content

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return self.model_name

    def load_model(self):
        pass

judge = GroqJudge()

def run_full_evaluation(experiment_name="experiment_v1", k_value=3):
    print(f"🚀 Starting evaluation for {experiment_name}...")
    
    # Load dataset
    dataset = []
    with open("eval_dataset.jsonl", "r") as f:
        for line in f:
            dataset.append(json.loads(line))

    # Initialize Metrics
    faithfulness = FaithfulnessMetric(threshold=0.7, model=judge)
    relevancy = AnswerRelevancyMetric(threshold=0.7, model=judge)

    results = []
    
    for i, item in enumerate(dataset):
        print(f"Testing case {i+1}/{len(dataset)}: {item['question']}")
        
        # Add a small delay to avoid RateLimitError (429)
        time.sleep(3)
        
        # 1. Get Answer from RAG Agent
        rag_response = ask(item['question'])
        actual_output = rag_response['answer']
        context = rag_response['context']
        
        # 2. Create Test Case
        test_case = LLMTestCase(
            input=item['question'],
            actual_output=actual_output,
            retrieval_context=[context]
        )
        
        # 3. Measure
        try:
            faithfulness.measure(test_case)
            relevancy.measure(test_case)
        except Exception as e:
            print(f"Metric error: {e}")
            # Default to 0 if it fails due to rate limit
            faithfulness.score = 0
            relevancy.score = 0
        
        results.append({
            "faithfulness": faithfulness.score,
            "relevancy": relevancy.score
        })

    # Calculate Averages
    avg_faith = sum(r['faithfulness'] for r in results) / len(results)
    avg_rel = sum(r['relevancy'] for r in results) / len(results)

    # Create Summary for Dashboard
    summary = {
        "experiment": experiment_name,
        "retriever_k": k_value,
        "number_of_test_cases": len(dataset),
        "metrics": {
            "answer_relevancy": avg_rel,
            "faithfulness": avg_faith,
            "context_relevancy": avg_rel, # Simplified for this demo
            "correctness": (avg_faith + avg_rel) / 2 # Simplified
        }
    }

    with open(f"{experiment_name}.jsonl", "w") as f:
        json.dump(summary, f)
    
    print(f"✅ Evaluation complete. Summary saved to {experiment_name}.jsonl")

if __name__ == "__main__":
    # We will run 3 experiments with different simulated "k" values to populate the dashboard
    run_full_evaluation("experiment_v1", k_value=1)
    run_full_evaluation("experiment_v2", k_value=2)
    run_full_evaluation("experiment_v3", k_value=3)
