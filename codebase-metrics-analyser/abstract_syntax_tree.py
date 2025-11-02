import ast
from pathlib import Path
import csv

from .metrics_visitor import MetricsVisitor


def iter_python_files(root_dir: str):
    for path in Path(root_dir).rglob("*.py"):
        if path.is_file():
            yield path

def parse_ast(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return ast.parse(f.read(), filename=str(path))
    except SyntaxError as e:
        return None

def analyse_codebase(root_dir: str):
    root_name = Path(*Path(root_dir).parts[-1:])

    for index, directory in enumerate(Path(root_dir).parts):
        if directory == str(root_name):
            break

    results = []

    for path in iter_python_files(root_dir):
        tree = parse_ast(path)
        if not tree:
            continue
        
        visitor = MetricsVisitor()
        visitor.visit(tree)

        directory_path = Path(*Path(path).parts[index:])

        for scope, data in visitor.metrics.items():
            results.append({
                "file": str(directory_path).replace("\\", "/"),
                "scope": scope,
                "assignments": data["assignments"],
                "statements": data["statements"],
                "expressions": data["expressions"],
            })
    
    return results



    


def write_metrics_csv(results, output_path: Path):
    if not (Path(__file__).resolve().parent.parent / 'results').exists():
        (Path(__file__).resolve().parent.parent / 'results').mkdir()

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
    
if __name__ == "__main__":
    metrics = analyse_codebase(
        str(Path(__file__).parent.parent.parent.resolve() / "discord.py")
    )

    script_dir = Path(__file__).parent
    output_file = script_dir.parent / "results" / "metrics.csv"

    write_metrics_csv(metrics, output_file)
