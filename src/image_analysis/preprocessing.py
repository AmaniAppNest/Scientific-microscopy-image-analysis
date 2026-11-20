from pathlib import Path

import numpy as np
import tifffile
from skimage import exposure
from skimage.filters import gaussian


def load_tiff_image(image_path: str | Path) -> np.ndarray:
    """Load a microscopy TIFF image."""
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    image = tifffile.imread(path)

    if image.ndim != 2:
        raise ValueError("Expected a single-channel, 2D microscopy image.")

    return image


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Scale image intensities to the range 0–1 for visualization."""
    if image.size == 0:
        raise ValueError("Input image is empty.")

    return exposure.rescale_intensity(
        image.astype(np.float32),
        in_range="image",
        out_range=(0.0, 1.0),
    )


def smooth_image(
    image: np.ndarray,
    sigma: float = 1.0,
) -> np.ndarray:
    """Reduce image noise using Gaussian smoothing."""
    if sigma <= 0:
        raise ValueError("Sigma must be greater than zero.")

    return gaussian(image, sigma=sigma, preserve_range=True)
