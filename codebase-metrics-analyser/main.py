from pathlib import Path


from .abstract_syntax_tree import analyse_codebase
from .write_metrics import write_metrics_csv
from .visualise import produce_treemap


REPOSITORY_NAME = "discord.py"

if __name__ == "__main__":
    current_path = Path(__file__).resolve()
        
    while True:
        parent_path = current_path.parent
        sibling_path = parent_path / REPOSITORY_NAME

        if sibling_path.is_dir():
            the_path = sibling_path
            break
            
        if parent_path == current_path:
            raise FileNotFoundError(
                f"'{REPOSITORY_NAME}' not found, starting from '{__file__}'."
            )
            
        current_path = parent_path

    metrics = analyse_codebase(the_path)

    script_dir = Path(__file__).parent
    output_file = script_dir.parent / "results" / "metrics.csv"

    write_metrics_csv(metrics, output_file)

    produce_treemap()
