from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from skimage.segmentation import find_boundaries


def save_segmentation_overlay(
    image: np.ndarray,
    labels: np.ndarray,
    output_path: str | Path,
) -> None:
    """Save the original image with segmentation boundaries overlaid."""

    if image.shape != labels.shape:
        raise ValueError("Image and labels must have the same dimensions.")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    boundaries = find_boundaries(labels, mode="outer")

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(image, cmap="gray")
    ax.imshow(
        np.ma.masked_where(~boundaries, boundaries),
        cmap="autumn",
        alpha=0.9,
    )
    ax.set_title("Watershed Segmentation Boundaries")
    ax.axis("off")

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {output_path}")


def save_label_image(
    labels: np.ndarray,
    output_path: str | Path,
) -> None:
    """Save a colour-coded image of segmented objects."""

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(labels, cmap="nipy_spectral")
    ax.set_title("Watershed Object Labels")
    ax.axis("off")

    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

    print(f"Saved: {output_path}")