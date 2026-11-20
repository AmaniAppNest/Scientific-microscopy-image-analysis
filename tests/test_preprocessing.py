import numpy as np
import pytest
import tifffile

from src.image_analysis.preprocessing import (
    load_tiff_image,
    normalize_image,
    smooth_image,
)


def test_load_tiff_image(tmp_path):
    image = np.ones((20, 30), dtype=np.uint16)
    image_path = tmp_path / "test.tif"
    tifffile.imwrite(image_path, image)

    loaded = load_tiff_image(image_path)

    assert loaded.shape == (20, 30)


def test_load_missing_image():
    with pytest.raises(FileNotFoundError):
        load_tiff_image("missing_image.tif")


def test_normalize_image():
    image = np.array([[0, 100], [200, 300]], dtype=np.uint16)

    normalized = normalize_image(image)

    assert normalized.min() == 0.0
    assert normalized.max() == 1.0


def test_normalize_empty_image():
    image = np.array([])

    with pytest.raises(ValueError):
        normalize_image(image)


def test_smooth_image():
    image = np.ones((20, 30))

    smoothed = smooth_image(image, sigma=1.0)

    assert smoothed.shape == image.shape


def test_smooth_invalid_sigma():
    image = np.ones((20, 30))

    with pytest.raises(ValueError):
        smooth_image(image, sigma=0)