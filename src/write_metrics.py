from pathlib import Path
import csv

def write_metrics_csv(results, output_path: Path):
    output_directory = (Path(__file__).resolve().parent.parent / 'results')
    if not output_directory.exists():
        output_directory.mkdir()

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "file",
            "scope",
            "assignments",
            "statements",
            "expressions",
        ])
        writer.writeheader()
        writer.writerows(results)
