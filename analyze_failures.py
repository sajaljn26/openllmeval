import json
import glob
import os

def analyze_failures(threshold=0.7):
    # The individual cases (with questions and answers) are stored in the results/ directory
    # The summary averages are in the experiments/ directory.
    result_files = glob.glob("results/results_experiment_v*.jsonl")
    failures = []

    if not result_files:
        print("No result files found in results/ directory.")
        return

    for file_path in result_files:
        experiment_name = os.path.basename(file_path).replace("results_", "").replace(".jsonl", "")
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                
                # Extract metrics
                metrics = {
                    "faithfulness": record.get("faithfulness", 0),
                    "relevancy": record.get("relevancy", 0),
                    "context_relevancy": record.get("context_relevancy", 0),
                    "correctness": record.get("correctness", 0)
                }
                
                # Flag as failure if any metric is below the threshold
                if any(score < threshold for score in metrics.values()):
                    failures.append({
                        "experiment": experiment_name,
                        "question": record.get("question", "N/A"),
                        "actual": record.get("actual", "N/A"),
                        "metrics": metrics
                    })

    # Write the analysis to failures.md
    with open("failures.md", "w", encoding="utf-8") as md_file:
        md_file.write("# 🚩 RAG Failure Analysis Report\n\n")
        md_file.write(f"Cases scoring below {threshold} on any metric.\n\n")
        
        if not failures:
            md_file.write("✅ No failures found! All cases are above the threshold.\n")
            return

        # Group failures by experiment for clarity
        experiments = sorted(list(set(f["experiment"] for f in failures)))
        
        for exp in experiments:
            md_file.write(f"## Experiment: {exp}\n\n")
            md_file.write("| Question | Answer | Faith | Rel | Ctx Rel | Corr |\n")
            md_file.write("| :--- | :--- | :--- | :--- | :--- | :--- |\n")
            
            exp_failures = [f for f in failures if f["experiment"] == exp]
            for fail in exp_failures:
                m = fail["metrics"]
                # Sanitize answer for markdown table
                clean_answer = fail["actual"].replace("\n", " ").replace("|", "\\|")
                if len(clean_answer) > 150:
                    clean_answer = clean_answer[:147] + "..."
                
                md_file.write(f"| {fail['question']} | {clean_answer} | {m['faithfulness']:.2f} | {m['relevancy']:.2f} | {m['context_relevancy']:.2f} | {m['correctness']:.2f} |\n")
            
            md_file.write("\n---\n\n")

    print(f"Analysis complete. Found {len(failures)} failing cases. Report saved to failures.md")

if __name__ == "__main__":
    analyze_failures()
