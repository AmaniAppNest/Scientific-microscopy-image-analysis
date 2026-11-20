import numpy as np
from scipy import ndimage as ndi
from skimage.filters import threshold_otsu
from skimage.measure import label
from skimage.morphology import remove_small_objects
from skimage.segmentation import watershed


def segment_otsu(
    image: np.ndarray,
    min_size: int = 30,
) -> np.ndarray:
    """Segment bright objects using Otsu thresholding."""
    if image.size == 0:
        raise ValueError("Input image is empty.")

    if min_size < 1:
        raise ValueError("Minimum object size must be positive.")

    threshold = threshold_otsu(image)
    mask = image > threshold

    return remove_small_objects(mask, max_size=min_size - 1)


def segment_watershed(
    mask: np.ndarray,
    min_distance: int = 10,
) -> np.ndarray:
    """Separate touching objects using watershed segmentation."""
    if mask.ndim != 2:
        raise ValueError("Expected a 2D binary mask.")

    if min_distance < 1:
        raise ValueError("Minimum distance must be positive.")

    distance = ndi.distance_transform_edt(mask)

    local_maxima = ndi.maximum_filter(
        distance,
        size=2 * min_distance + 1,
    ) == distance

    markers = label(local_maxima & mask)

    return watershed(
        -distance,
        markers,
        mask=mask,
    )