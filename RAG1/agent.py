import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from .tools import collecting_info
from .prompts import system_agent_prompt
import RAG1.tools as tl

load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b", 
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Simple RAG Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", system_agent_prompt),
    ("human", "Context: {context}\n\nQuestion: {input}"),
])

def ask(question: str) -> dict:
    """ 
    A clean RAG implementation: 
    1. Retrieves context using the tool
    2. Generates an answer using the LLM
    """
    
    # 1. Retrieve context
    try:
        context_text = collecting_info.invoke(question)
    except Exception as e:
        context_text = "No relevant context found."
    
    # Save for evaluation purposes
    tl.last_retrieved_context = [context_text]

    # 2. Generate answer
    chain = prompt | llm
    try:
        response = chain.invoke({
            "context": context_text,
            "input": question
        })
        answer_text = response.content
    except Exception as e:
        answer_text = f"Error during generation: {str(e)}"

    return {
        "answer": answer_text,
        "context": context_text
    }
