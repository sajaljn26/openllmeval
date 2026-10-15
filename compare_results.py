import json
import glob
import os

def compare_results():
    # Path to the results files
    result_files = glob.glob("results/results_experiment_v*.jsonl")
    
    if not result_files:
        print("No result files found in results/ directory.")
        return

    metrics_keys = ["faithfulness", "relevancy", "context_relevancy", "correctness"]
    summary_data = []

    for file_path in sorted(result_files):
        experiment_name = os.path.basename(file_path).replace("results_", "").replace(".jsonl", "")
        
        total_cases = 0
        judge_errors = 0
        
        # Totals for all cases
        all_sums = {k: 0.0 for k in metrics_keys}
        # Totals for non-error cases
        valid_sums = {k: 0.0 for k in metrics_keys}
        valid_count = 0

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                
                record = json.loads(line)
                total_cases += 1
                
                # Extract scores
                scores = {k: record.get(k, 0.0) for k in metrics_keys}
                
                # Identify Judge Error: All metrics are exactly 0
                if all(val == 0 for val in scores.values()):
                    judge_errors += 1
                else:
                    valid_count += 1
                
                # Add to all sums
                for k in metrics_keys:
                    all_sums[k] += scores[k]
                    if all(val == 0 for val in scores.values()) == False:
                        valid_sums[k] += scores[k]

        # Calculate Averages
        all_avgs = {k: (all_sums[k] / total_cases if total_cases > 0 else 0) for k in metrics_keys}
        valid_avgs = {k: (valid_sums[k] / valid_count if valid_count > 0 else 0) for k in metrics_keys}

        summary_data.append({
            "experiment": experiment_name,
            "total": total_cases,
            "errors": judge_errors,
            "all_avgs": all_avgs,
            "valid_avgs": valid_avgs
        })

    # Construct Markdown Table
    header = "| Experiment | Total | Judge Errors | Metric | Avg (All) | Avg (Excl. Errors) |\n"
    separator = "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    rows = ""
    for data in summary_data:
        exp = data["experiment"]
        tot = data["total"]
        err = data["errors"]
        
        for k in metrics_keys:
            # Format metric name for readability
            display_name = k.replace("_", " ").title()
            val_all = data["all_avgs"][k]
            val_valid = data["valid_avgs"][k]
            rows += f"| {exp} | {tot} | {err} | {display_name} | {val_all:.3f} | {val_valid:.3f} |\n"
        rows += "\n"

    with open("results/summary.md", "w", encoding="utf-8") as md_file:
        md_file.write("# 📊 Experiment Comparison Summary\n\n")
        md_file.write("This table compares the performance of different experiments, highlighting the impact of 'Judge Errors' (cases where all metrics were 0).\n\n")
        md_file.write(header + separator + rows)

    print(f"Comparison complete. Summary saved to results/summary.md")

if __name__ == "__main__":
    compare_results()
