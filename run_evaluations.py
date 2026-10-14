import os
import json
import time
from dotenv import load_dotenv
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric, ContextualRelevancyMetric, GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_groq import ChatGroq
from RAG1.agent import ask

load_dotenv()

# --- DeepEval Groq Judge Setup ---
class GroqJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="qwen/qwen3.8-27b"):
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
    ctx_relevancy = ContextualRelevancyMetric(threshold=0.7, model=judge)
    correctness = GEval(
        name="Correctness",
        criteria="Determine whether the actual output is factually correct based on the expected output.",
        evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT, SingleTurnParams.EXPECTED_OUTPUT],
        model=judge,
        threshold=0.7
    )

    results = []
    individual_results = []
    
    for i, item in enumerate(dataset):
        print(f"Testing case {i+1}/{len(dataset)}: {item['question']}")
        
        # Add a small delay to avoid RateLimitError (429)
        time.sleep(2)
        
        # 1. Get Answer from RAG Agent
        rag_response = ask(item['question'], k=k_value)
        actual_output = rag_response['answer']
        context = rag_response['context']
        
        # 2. Create Test Case
        test_case = LLMTestCase(
            input=item['question'],
            actual_output=actual_output,
            expected_output=item['expected_answer'],
            retrieval_context=[context]
        )
        
        # 3. Measure
        try:
            faithfulness.measure(test_case)
            relevancy.measure(test_case)
            ctx_relevancy.measure(test_case)
            correctness.measure(test_case)
        except Exception as e:
            print(f"⚠️ Metric error on case {i+1}: {e}")
            faithfulness.score = 0
            relevancy.score = 0
            ctx_relevancy.score = 0
            correctness.score = 0
        
        score_faith = faithfulness.score
        score_rel = relevancy.score
        score_ctx = ctx_relevancy.score
        score_corr = correctness.score
        
        results.append({
            "faithfulness": score_faith,
            "relevancy": score_rel,
            "context_relevancy": score_ctx,
            "correctness": score_corr
        })

        individual_results.append({
            "question": item['question'],
            "expected": item['expected_answer'],
            "actual": actual_output,
            "context": context,
            "faithfulness": score_faith,
            "relevancy": score_rel,
            "context_relevancy": score_ctx,
            "correctness": score_corr
        })

    # Save individual results for this experiment
    with open(f"results_{experiment_name}.jsonl", "w") as f:
        for res in individual_results:
            f.write(json.dumps(res) + "\n")


    # Calculate Averages
    avg_faith = sum(r['faithfulness'] for r in results) / len(results)
    avg_rel = sum(r['relevancy'] for r in results) / len(results)
    avg_ctx = sum(r['context_relevancy'] for r in results) / len(results)
    avg_corr = sum(r['correctness'] for r in results) / len(results)

    # Create Summary for Dashboard
    summary = {
        "experiment": experiment_name,
        "retriever_k": k_value,
        "number_of_test_cases": len(dataset),
        "metrics": {
            "answer_relevancy": avg_rel,
            "faithfulness": avg_faith,
            "context_relevancy": avg_ctx,
            "correctness": avg_corr
        }
    }

    with open(f"{experiment_name}.jsonl", "w") as f:
        json.dump(summary, f)
    
    print(f"✅ Evaluation complete. Summary saved to {experiment_name}.jsonl")

if __name__ == "__main__":
    run_full_evaluation("experiment_v1", k_value=1)
    run_full_evaluation("experiment_v2", k_value=2)
    run_full_evaluation("experiment_v3", k_value=3)
