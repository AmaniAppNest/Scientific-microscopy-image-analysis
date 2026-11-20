from pathlib import Path

from src.image_analysis.preprocessing import (
    load_tiff_image,
    normalize_image,
    smooth_image,
)
from src.image_analysis.segmentation import (
    segment_otsu,
    segment_watershed,
)
from src.image_analysis.feature_extraction import extract_features
from src.image_analysis.evaluation import evaluate_segmentation
from src.image_analysis.visualization import (
    save_segmentation_overlay,
    save_label_image,
)
from src.image_analysis.report import generate_report


def main():
    # Project paths
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    image_files = sorted(Path(".").glob("*.tif"))

    if not image_files:
        raise FileNotFoundError("No TIFF images found in the project directory.")

    image_path = image_files[0]
    print(f"Processing image: {image_path.name}")

    # 1. Load and preprocess image
    image = load_tiff_image(image_path)
    normalized = normalize_image(image)
    smoothed = smooth_image(normalized, sigma=2.0)

    # 2. Segment objects
    mask = segment_otsu(smoothed)
    labels = segment_watershed(mask, min_distance=15)

    # 3. Extract object measurements
    measurements = extract_features(
        image,
        labels,
        output_dir / "object_measurements.csv",
    )

    # 4. Generate quality-control summary
    evaluate_segmentation(labels, measurements)

    # 5. Save visualizations
    save_segmentation_overlay(
        image,
        labels,
        output_dir / "segmentation_overlay.png",
    )
    save_label_image(
        labels,
        output_dir / "segmentation_labels.png",
    )

    # 6. Generate statistical report
    generate_report()

    print("\nImage analysis pipeline completed successfully.")


if __name__ == "__main__":
    main()