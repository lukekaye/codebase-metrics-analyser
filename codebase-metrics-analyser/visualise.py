import plotly.express as px
import pandas as pd
from pathlib import Path

def produce_treemap():
    csv_path = Path("results/metrics.csv")
    output_json_path = Path("metrics_treemap.json")

    if not csv_path.exists():
        raise FileNotFoundError(f"{csv_path} not found")
    df = pd.read_csv("results/metrics.csv")

    metric_cols = [
        "assignments",
        "statements",
        "expressions",
    ]
    for col in metric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    df["statements_per_expression"] = (
        df["statements"] / df["expressions"]
    ).fillna(0).replace([float('inf'), float('-inf')], 0)

    df["assignments_per_expression"] = (
        df["assignments"] / df["expressions"]
    ).fillna(0).replace([float('inf'), float('-inf')], 0)

    df["custom_hover_text"] = df.apply(
        lambda row: (
            f"-----------------<br>"
            f"Expressions: {int(row['expressions'])}<br>"
            f"Statements: {int(row['statements'])}<br>"
            f"Assignments: {int(row['assignments'])}<br>"
            f"Statements per Expression: {row['statements_per_expression']:.2f}<br>"
            f"Assignments per Expression: {row['assignments_per_expression']:.2f}"
        ),
        axis=1
    )

    COLOR_OPTIONS = {
        "Statements / Expressions (Low Density)": {
            "column": "statements_per_expression", 
            "title": "Low Density Ratio (Statements / Expressions)",
            "max_value": df["statements_per_expression"].quantile(0.95), 
        },
        "Assignments / Expressions (Assignment Use)": {
            "column": "assignments_per_expression",
            "title": "Assignment Density (Assignments / Expressions)",
            "max_value": df["assignments_per_expression"].quantile(0.95),
        },
        "Expressions (Absolute Size)": {
            "column": "expressions",
            "title": "Absolute Size (Expressions)",
            "max_value": df["expressions"].max(),
        },
    }

    buttons = []
    for label, data in COLOR_OPTIONS.items():
        button = dict(
            args=[
                {
                    "marker.colors": [df[data["column"]].tolist()], 
                    "marker.colorbar.title": data["title"],
                    "marker.cmax": data["max_value"],
                    "title.text": f"Size=Statements, Color={label}", 
                }
            ],
            label=label,
            method="restyle",
        )
        buttons.append(button)

    updatemenus = [
        dict(
            type="dropdown",
            direction="down",
            active=0,
            x=1.1,
            y=1.15,
            buttons=buttons,
            pad={"r": 10, "t": 10},
            showactive=True,
        )
    ]

    CUSTOM_DATA_COLS = ["custom_hover_text"]

    default_color_col = "statements_per_expression"
    fig = px.treemap(
        df,
        path=["file", "scope"],
        values="expressions",
        color=default_color_col,
        color_continuous_scale="Viridis",
    )

    if fig.data:
        fig.data[0].customdata = df["custom_hover_text"].values

        fig.data[0].hovertemplate = (
            "<b>%{label}</b><br>"
            "Path: %{currentPath}<br>"
            "Total Statements (Aggregated): %{value}<br>"
            "%{customdata}" 
            "<extra></extra>" 
        )
        
        fig.data[0].texttemplate = ""
        fig.data[0].textinfo = "none"

    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        updatemenus=updatemenus,
        coloraxis_colorbar_title_text="Ratio"
    )
    # fig.write_json(output_json_path)

    fig.show()
