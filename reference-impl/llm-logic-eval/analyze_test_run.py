import argparse
import csv
import os
import re
import sys
from typing import Dict, List, Optional

def extract_tag(content: str, tag: str) -> Optional[str]:
    match = re.search(rf"<{tag}>(.*?)</{tag}>", content, re.DOTALL)
    return match.group(1).strip() if match else None

def parse_test_output(file_path: str) -> Dict[str, Optional[object]]:
    """
    Parse an output file produced by test_puzzle.
    
    Returns:
        {
            "num_people": int | None,
            "num_attributes": int | None,
            "response_correct": bool | None,
            "exception": str | None,
        }
    """
    with open(file_path, "r") as f:
        content = f.read()

    num_people_raw = extract_tag(content, "num_people")
    num_attributes_raw = extract_tag(content, "num_attributes")
    response_correct_raw = extract_tag(content, "response_correct")
    exception_raw = extract_tag(content, "exception")

    num_people = int(num_people_raw) if num_people_raw is not None else None
    num_attributes = int(num_attributes_raw) if num_attributes_raw is not None else None
    response_correct = None
    if response_correct_raw is not None:
        response_correct = response_correct_raw.lower() == "true"

    return {
        "num_people": num_people,
        "num_attributes": num_attributes,
        "response_correct": response_correct,
        "exception": exception_raw,
    }


def parse_all_test_outputs(outputs_dir: str) -> List[Dict[str, Optional[object]]]:
    """
    Parse all test output files in the given outputs directory.
    
    Returns:
        List of dictionaries, each including filename and parsed fields.
    """
    results = []
    for name in sorted(os.listdir(outputs_dir)):
        file_path = os.path.join(outputs_dir, name)
        try:
            parsed = parse_test_output(file_path)
            parsed_with_name = {"filename": name, **parsed}
            results.append(parsed_with_name)
        except Exception as e:
            results.append({
                "filename": name,
                "num_people": None,
                "num_attributes": None,
                "response_correct": None,
                "exception": f"Failed to parse: {e}",
            })
    return results

def analyze_test_outputs(test_outputs, output_dir):
    """
    Compute pass rates grouped by (num_people, num_attributes) and
    write them to a CSV that includes total runs, exception counts,
    valid runs, passed count, and pass rate.
    """
    stats = {}
    people_vals = set()
    attr_vals = set()
    for entry in test_outputs:
        print(entry)
        num_people = entry.get("num_people")
        num_attrs = entry.get("num_attributes")
        exception = entry.get("exception")
        response_correct = entry.get("response_correct")

        people_vals.add(num_people)
        attr_vals.add(num_attrs)

        key = (num_people, num_attrs)
        if key not in stats:
            stats[key] = {"passed": 0, "valid_runs": 0, "total_runs": 0, "exception_count": 0}

        # Count all runs
        stats[key]["total_runs"] += 1
        
        # Count exceptions
        if exception is not None:
            stats[key]["exception_count"] += 1
        else:
            # Only count tests without exceptions as valid
            stats[key]["valid_runs"] += 1
            if response_correct is True:
                stats[key]["passed"] += 1

    # Compute pass_rate
    for key, val in stats.items():
        if val["valid_runs"] > 0:
            val["pass_rate"] = val["passed"] / val["valid_runs"]
        else:
            val["pass_rate"] = None

    # Write CSV with separate grids for each metric
    people_list = sorted(people_vals)
    attr_list = sorted(attr_vals)

    csv_path = os.path.join(output_dir, "pass_rates.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        
        # Pass Rate
        writer.writerow(["Pass Rate"])
        writer.writerow(["num_people \\ num_attributes"] + [str(a) for a in attr_list])
        for p in people_list:
            row = [str(p)]
            for a in attr_list:
                key = (p, a)
                if key in stats and stats[key]["pass_rate"] is not None:
                    row.append(f"{stats[key]['pass_rate']:.3f}")
                else:
                    row.append("")
            writer.writerow(row)

        # Passed Runs
        writer.writerow(["Passed Runs"])
        writer.writerow(["num_people \\ num_attributes"] + [str(a) for a in attr_list])
        for p in people_list:
            row = [str(p)]
            for a in attr_list:
                key = (p, a)
                if key in stats:
                    row.append(str(stats[key]["passed"]))
                else:
                    row.append("")
            writer.writerow(row)
        writer.writerow([])  # Empty row separator
        
        # Total Runs
        writer.writerow(["Total Runs"])
        writer.writerow(["num_people \\ num_attributes"] + [str(a) for a in attr_list])
        for p in people_list:
            row = [str(p)]
            for a in attr_list:
                key = (p, a)
                if key in stats:
                    row.append(str(stats[key]["total_runs"]))
                else:
                    row.append("")
            writer.writerow(row)
        writer.writerow([])  # Empty row separator
        
        # Exception Count
        writer.writerow(["Exception Count"])
        writer.writerow(["num_people \\ num_attributes"] + [str(a) for a in attr_list])
        for p in people_list:
            row = [str(p)]
            for a in attr_list:
                key = (p, a)
                if key in stats:
                    row.append(str(stats[key]["exception_count"]))
                else:
                    row.append("")
            writer.writerow(row)
        writer.writerow([])  # Empty row separator
        
    return stats

def main():
    parser = argparse.ArgumentParser(description='Analyze test outputs from logic puzzle generator')
    parser.add_argument('-outputs_dir', '-o', type=str, default='outputs',
                       help='Directory containing the test output files to analyze')
    parser.add_argument('-results-dir', '-r', type=str, default='.',
                       help='Directory to save the results CSV (default: current directory)')
    
    args = parser.parse_args()
    test_outputs = parse_all_test_outputs(args.outputs_dir)
    stats = analyze_test_outputs(test_outputs, args.results_dir)
    print(stats)

if __name__ == "__main__":
    main()