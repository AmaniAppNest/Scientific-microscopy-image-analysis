"""Generate visual summaries of measured image objects."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def generate_report() -> None:
    """Create distribution plots from the object measurements CSV."""
    project_root = Path(__file__).resolve().parents[2]
    csv_path = project_root / "results" / "object_measurements.csv"
    output_dir = project_root / "results"

    if not csv_path.exists():
        raise FileNotFoundError(f"Measurements file not found: {csv_path}")

    data = pd.read_csv(csv_path)

    required_columns = ["area", "mean_intensity", "eccentricity"]
    missing = [column for column in required_columns if column not in data.columns]

    if missing:
        raise ValueError(f"CSV is missing required columns: {missing}")

    plots = [
        ("area", "Object area (pixels)", "Object area distribution",
         "area_distribution.png"),
        ("mean_intensity", "Mean intensity", "Mean intensity distribution",
         "intensity_distribution.png"),
        ("eccentricity", "Eccentricity (0–1)", "Object shape distribution",
         "shape_distribution.png"),
    ]

    for column, xlabel, title, filename in plots:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(data[column].dropna(), bins=20, edgecolor="black")
        ax.set_xlabel(xlabel)
        ax.set_ylabel("Number of objects")
        ax.set_title(title)
        fig.tight_layout()
        fig.savefig(output_dir / filename, dpi=300)
        plt.close(fig)

        print(f"Saved: results/{filename}")

    print(f"Report generated for {len(data)} objects.")


if __name__ == "__main__":
    generate_report()
