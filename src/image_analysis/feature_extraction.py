from pathlib import Path

import numpy as np
import pandas as pd
from skimage.measure import regionprops_table


def extract_features(
    image: np.ndarray,
    labels: np.ndarray,
    output_path: str | Path,
) -> pd.DataFrame:
    """Extract morphological and intensity measurements from segmented objects."""

    if image.shape != labels.shape:
        raise ValueError("Image and labels must have the same dimensions.")

    features = regionprops_table(
        labels,
        intensity_image=image,
        properties=(
            "label",
            "area",
            "centroid",
            "eccentricity",
            "solidity",
            "mean_intensity",
        ),
    )

    data = pd.DataFrame(features)

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(output_path, index=False)

    print(f"Saved measurements: {output_path}")
    print(f"Measured objects: {len(data)}")

    return data