import os
from dotenv import load_dotenv
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase
from deepeval.models.base_model import DeepEvalBaseLLM

load_dotenv()

# Create a custom Groq Model for DeepEval to use as a judge
class GroqJudge(DeepEvalBaseLLM):
    def __init__(self, model_name="openai/gpt-oss-20b"):
        self.model_name = model_name
        from langchain_groq import ChatGroq
        self.llm = ChatGroq(model_name=self.model_name, groq_api_key=os.getenv("GROQ_API_KEY"))

    def generate(self, prompt: str) -> str:
        # DeepEval expects a string response from the judge
        response = self.llm.invoke(prompt)
        return response.content

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return self.model_name

    def load_model(self):
        pass

# Set the judge
judge = GroqJudge()

def test_faithfulness():
    # Example test case
    test_case = LLMTestCase(
        input="What is the diet of penguins?",
        actual_output="Penguins primarily eat fish and krill.",
        retrieval_context=["Penguins are carnivorous birds that feed on fish, squid, and krill."]
    )
    
    # Initialize metric with our Groq judge
    metric = FaithfulnessMetric(threshold=0.7, model=judge)
    metric.measure(test_case)
    
    print(f"Faithfulness Score: {metric.score}")
    print(f"Reason: {metric.reason}")

if __name__ == "__main__":
    test_faithfulness()
