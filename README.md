# Open LLM Evaluation System

A professional framework for the systematic evaluation of Retrieval-Augmented Generation (RAG) pipelines. This project provides a complete environment to ingest documents, retrieve context, generate responses using high-performance open-source LLMs, and quantify performance using industry-standard metrics.

## 📌 Overview

Evaluating LLMs often suffers from subjectivity. This system replaces qualitative "manual testing" with quantitative metrics. By leveraging **DeepEval**, the system implements an "LLM-as-a-Judge" pattern to provide a mathematical score for the quality of the RAG pipeline.

## 🛠️ Technical Stack

### Core Architecture
- **LLM Inference:** [Groq](https://groq.com/) (Llama-3 / Mixtral) for low-latency, high-throughput generation.
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace for efficient local vectorization.
- **Vector Database:** **FAISS** (Facebook AI Similarity Search) for optimized similarity search.
- **Evaluation Framework:** **DeepEval** for calculating RAG-specific metrics.
- **Frontend:** **Streamlit** for a centralized evaluation dashboard.

### Pipeline Flow
`PDF Document` $\rightarrow$ `Text Extraction (PyMuPDF)` $\rightarrow$ `Embedding Generation` $\rightarrow$ `FAISS Indexing` $\rightarrow$ `Context Retrieval` $\rightarrow$ `Groq LLM Generation` $\rightarrow$ `Metric Scoring (DeepEval)` $\rightarrow$ `Visualization (Streamlit)`

---

## 📊 Evaluation Metrics

The system measures four key performance indicators (KPIs) to identify bottlenecks in the RAG pipeline:

| Metric | Description | Purpose |
| :--- | :--- | :--- |
| **Faithfulness** | Measures if the answer is derived solely from the retrieved context. | Detects **Hallucinations**. |
| **Answer Relevancy** | Evaluates how well the answer addresses the original user query. | Detects **Irrelevant Outputs**. |
| **Context Relevancy** | Measures the proportion of retrieved context that is useful for the query. | Detects **Retrieval Inefficiency**. |
| **Correctness** | Compares the generated answer against a provided ground-truth answer. | Detects **Factual Inaccuracy**. |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Groq API Key ([Get one here](https://console.groq.com/))

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Open-LLM-Evaluation-System.git
   cd Open-LLM-Evaluation-System
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

### Execution
1. **Run Evaluations:**
   Generate evaluation results for multiple experiments (different $k$ values):
   ```bash
   python run_evaluations.py
   ```
2. **Launch Dashboard:**
   Visualize the metrics and compare runs:
   ```bash
   streamlit run dashboard.py
   ```

---

## 📂 Project Structure

```text
Open_LLM_Eval_System/
├── RAG1/               # Core RAG Pipeline
│   ├── agent.py        # LLM logic and chain orchestration
│   ├── indexing.py      # Embedding and FAISS setup
│   ├── tools.py        # Retrieval tools
│   └── prompts.py      # System prompts for the agent
├── pdfs/               # Source documents for retrieval
├── single_tests/       # Unit tests for individual metrics
├── run_evaluations.py   # Main evaluation runner
├── dashboard.py        # Streamlit visualization app
└── requirements.txt    # Project dependencies
```

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for more information.
