import numpy as np
import pandas as pd


def evaluate_segmentation(
    labels: np.ndarray,
    measurements: pd.DataFrame,
) -> dict:
    """Generate basic quality-control statistics for a segmentation."""

    if labels.ndim != 2:
        raise ValueError("Expected a 2D label image.")

    object_count = int(labels.max())
    foreground_pixels = int(np.count_nonzero(labels))

    object_areas = measurements["area"] if not measurements.empty else []

    summary = {
        "object_count": object_count,
        "foreground_pixels": foreground_pixels,
        "mean_object_area": (
            float(np.mean(object_areas)) if len(object_areas) else 0.0
        ),
    }

    print("Segmentation quality-control summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")

    return summary