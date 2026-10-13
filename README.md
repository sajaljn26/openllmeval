# Open LLM Evaluation System

This is an open-source implementation of a RAG (Retrieval-Augmented Generation) evaluation lab. It demonstrates how to build, test, and evaluate an LLM pipeline using high-performance open-source tools.

## 🚀 Tech Stack
- **LLM:** `Llama-3` via **Groq** (High-speed inference)
- **Embeddings:** `all-MiniLM-L6-v2` via **HuggingFace** (Local, free embeddings)
- **Vector Store:** **FAISS** (Efficient similarity search)
- **Evaluation:** **DeepEval** (Configured with Groq as the LLM judge)
- **Framework:** **LangChain**
- **Dashboard:** **Streamlit**

## 🛠️ Architecture
1. **Knowledge Base:** A PDF document is processed and split into chunks.
2. **Indexing:** Chunks are embedded using a HuggingFace model and stored in a FAISS index.
3. **RAG Agent:** A LangChain agent uses `Llama-3` to retrieve relevant context and generate answers.
4. **Evaluation:** The system uses **DeepEval** to score the output based on:
   - **Faithfulness:** Is the answer derived solely from the retrieved context?
   - **Answer Relevancy:** Does the answer actually address the user's question?
   - **Context Relevancy:** Was the retrieved context actually useful?
   - **Correctness:** Is the answer factually correct compared to a ground truth?

## 🏁 Getting Started

### 1. Requirements
- Python 3.10+
- A **Groq API Key** (Get one for free at [console.groq.com](https://console.groq.com))

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

### 4. Running the Project
- **Test the Agent:** Create a small script to call `RAG1.agent.ask("your question")`.
- **Run Evaluations:** Execute the scripts in `single_tests/` to see how the metrics work.
- **Launch Dashboard:**
```bash
streamlit run dashboard.py
```

## 🌟 Why this is great for a Resume
- **Cost Optimization:** Replaces expensive OpenAI calls with free/cheap open-source alternatives.
- **Performance:** Leverages Groq for near-instantaneous response times.
- **Rigorous Testing:** Implements industry-standard evaluation metrics (DeepEval) rather than just "vibes-based" testing.
- **Full Stack AI:** Covers the entire pipeline: Data ingestion -> Embedding -> Retrieval -> Generation -> Evaluation -> Visualization.
