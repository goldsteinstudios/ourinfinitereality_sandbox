"""
GlyphImageProcessor: Image processing for CHUBS glyph images.

Handles loading, normalizing, binarizing, and preparing glyph images
for tracing and feature extraction.
"""

import os
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
import json

# Optional imports - gracefully degrade if not available
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    np = None

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    Image = None


class GlyphImageProcessor:
    """
    Process CHUBS glyph images for font creation.

    Handles:
    - Loading images from CHUBS dataset
    - Normalization and binarization
    - Cropping to content
    - Size standardization
    - Contour extraction (if scikit-image available)
    """

    DEFAULT_SIZE = 128  # Standard output size
    DEFAULT_PADDING = 4  # Padding around content

    def __init__(self, chubs_dir: Optional[Path] = None):
        """
        Initialize the processor.

        Args:
            chubs_dir: Path to CHUBS dataset. Defaults to data/CHUBS_repo/
        """
        if chubs_dir is None:
            self.chubs_dir = Path(__file__).parent.parent.parent / "data" / "CHUBS_repo"
        else:
            self.chubs_dir = Path(chubs_dir)

        self.glyphs_dir = self.chubs_dir / "glyphs"

        # Check dependencies
        if not HAS_PIL:
            print("Warning: PIL not available. Image loading will be limited.")
        if not HAS_NUMPY:
            print("Warning: NumPy not available. Image processing will be limited.")

    def get_glyph_folder(self, character: str) -> Optional[Path]:
        """
        Find the glyph folder for a character in CHUBS.

        Args:
            character: The Chinese character

        Returns:
            Path to glyph folder or None if not found
        """
        if not self.glyphs_dir.exists():
            return None

        # Direct match
        direct = self.glyphs_dir / character
        if direct.exists():
            return direct

        # Search for variants (e.g., "道" might be in "迵（道）")
        for folder in self.glyphs_dir.iterdir():
            if folder.is_dir():
                # Check if character appears in folder name
                if character in folder.name:
                    return folder
                # Check for parenthetical notation
                if f"（{character}）" in folder.name or f"({character})" in folder.name:
                    return folder

        return None

    def list_glyph_images(self, character: str) -> List[Path]:
        """
        List all glyph images for a character.

        Args:
            character: The Chinese character

        Returns:
            List of image file paths
        """
        folder = self.get_glyph_folder(character)
        if not folder:
            return []

        images = []
        for ext in ['*.png', '*.jpg', '*.jpeg', '*.bmp']:
            images.extend(folder.glob(ext))

        return sorted(images)

    def load_image(self, image_path: Path) -> Optional[Any]:
        """
        Load an image file.

        Args:
            image_path: Path to image file

        Returns:
            PIL Image or None if loading fails
        """
        if not HAS_PIL:
            return None

        try:
            return Image.open(image_path)
        except Exception as e:
            print(f"Error loading {image_path}: {e}")
            return None

    def to_array(self, image: Any) -> Optional[Any]:
        """
        Convert PIL Image to numpy array.

        Args:
            image: PIL Image

        Returns:
            numpy array or None
        """
        if not HAS_NUMPY or not HAS_PIL:
            return None

        return np.array(image)

    def to_grayscale(self, arr: Any) -> Any:
        """
        Convert array to grayscale.

        Args:
            arr: numpy array (RGB or RGBA)

        Returns:
            Grayscale array
        """
        if not HAS_NUMPY:
            return arr

        if len(arr.shape) == 2:
            return arr  # Already grayscale

        if arr.shape[2] == 4:
            # RGBA - use alpha channel or convert
            return np.mean(arr[:, :, :3], axis=2).astype(np.uint8)
        elif arr.shape[2] == 3:
            # RGB - standard grayscale conversion
            return (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype(np.uint8)

        return arr

    def binarize(self, arr: Any, method: str = "otsu", threshold: int = 128) -> Any:
        """
        Binarize grayscale image.

        Args:
            arr: Grayscale numpy array
            method: "otsu" for automatic threshold, "fixed" for manual
            threshold: Fixed threshold value (0-255) if method="fixed"

        Returns:
            Binary array (0 or 255)
        """
        if not HAS_NUMPY:
            return arr

        if method == "otsu":
            # Simple Otsu's method implementation
            hist, _ = np.histogram(arr.flatten(), bins=256, range=(0, 256))
            total = arr.size

            sum_total = np.sum(np.arange(256) * hist)
            sum_bg = 0
            weight_bg = 0
            max_var = 0
            best_thresh = 0

            for t in range(256):
                weight_bg += hist[t]
                if weight_bg == 0:
                    continue

                weight_fg = total - weight_bg
                if weight_fg == 0:
                    break

                sum_bg += t * hist[t]
                mean_bg = sum_bg / weight_bg
                mean_fg = (sum_total - sum_bg) / weight_fg

                var_between = weight_bg * weight_fg * (mean_bg - mean_fg) ** 2

                if var_between > max_var:
                    max_var = var_between
                    best_thresh = t

            threshold = best_thresh

        binary = np.where(arr > threshold, 255, 0).astype(np.uint8)
        return binary

    def crop_to_content(self, arr: Any, padding: int = None) -> Any:
        """
        Crop array to non-white content with padding.

        Args:
            arr: Binary or grayscale array
            padding: Padding pixels around content

        Returns:
            Cropped array
        """
        if not HAS_NUMPY:
            return arr

        if padding is None:
            padding = self.DEFAULT_PADDING

        # Find non-white pixels (assuming white background = 255)
        if len(arr.shape) == 2:
            content_mask = arr < 250
        else:
            content_mask = np.any(arr < 250, axis=2)

        rows = np.any(content_mask, axis=1)
        cols = np.any(content_mask, axis=0)

        if not np.any(rows) or not np.any(cols):
            return arr  # No content found

        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]

        # Add padding
        rmin = max(0, rmin - padding)
        rmax = min(arr.shape[0], rmax + padding + 1)
        cmin = max(0, cmin - padding)
        cmax = min(arr.shape[1], cmax + padding + 1)

        return arr[rmin:rmax, cmin:cmax]

    def normalize_size(self, arr: Any, size: int = None) -> Any:
        """
        Resize array to standard square size while preserving aspect ratio.

        Args:
            arr: Input array
            size: Target size (width and height)

        Returns:
            Resized array
        """
        if not HAS_NUMPY or not HAS_PIL:
            return arr

        if size is None:
            size = self.DEFAULT_SIZE

        # Convert to PIL for resizing
        if len(arr.shape) == 2:
            img = Image.fromarray(arr, mode='L')
        else:
            img = Image.fromarray(arr)

        # Calculate new size preserving aspect ratio
        h, w = arr.shape[:2]
        if h > w:
            new_h = size
            new_w = int(w * size / h)
        else:
            new_w = size
            new_h = int(h * size / w)

        # Resize
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Create square canvas and center
        if len(arr.shape) == 2:
            canvas = Image.new('L', (size, size), 255)
        else:
            canvas = Image.new('RGB', (size, size), (255, 255, 255))

        x_offset = (size - new_w) // 2
        y_offset = (size - new_h) // 2
        canvas.paste(img, (x_offset, y_offset))

        return np.array(canvas)

    def process_for_tracing(self, image_path: Path) -> Dict[str, Any]:
        """
        Full processing pipeline for a glyph image.

        Args:
            image_path: Path to source image

        Returns:
            Dict with processed image data and metadata
        """
        result = {
            "source_path": str(image_path),
            "success": False,
            "error": None,
            "processed_array": None,
            "metadata": {}
        }

        # Load
        img = self.load_image(image_path)
        if img is None:
            result["error"] = "Failed to load image"
            return result

        result["metadata"]["original_size"] = img.size
        result["metadata"]["mode"] = img.mode

        # Convert to array
        arr = self.to_array(img)
        if arr is None:
            result["error"] = "Failed to convert to array"
            return result

        # Process
        gray = self.to_grayscale(arr)
        binary = self.binarize(gray, method="otsu")
        cropped = self.crop_to_content(binary)
        normalized = self.normalize_size(cropped)

        result["processed_array"] = normalized
        result["metadata"]["processed_size"] = normalized.shape
        result["success"] = True

        return result

    def save_processed(self, arr: Any, output_path: Path) -> bool:
        """
        Save processed array as image.

        Args:
            arr: numpy array
            output_path: Where to save

        Returns:
            True if successful
        """
        if not HAS_PIL or not HAS_NUMPY:
            return False

        try:
            if len(arr.shape) == 2:
                img = Image.fromarray(arr, mode='L')
            else:
                img = Image.fromarray(arr)

            output_path.parent.mkdir(parents=True, exist_ok=True)
            img.save(output_path)
            return True
        except Exception as e:
            print(f"Error saving to {output_path}: {e}")
            return False

    def get_image_quality_score(self, image_path: Path) -> float:
        """
        Calculate a quality score for a glyph image.

        Factors:
        - Contrast (higher = better)
        - Ink coverage (middle range = better)
        - Edge clarity (fewer artifacts = better)

        Args:
            image_path: Path to image

        Returns:
            Quality score 0-1
        """
        if not HAS_NUMPY or not HAS_PIL:
            return 0.5  # Default if deps missing

        img = self.load_image(image_path)
        if img is None:
            return 0.0

        arr = self.to_array(img)
        gray = self.to_grayscale(arr)

        # Contrast: standard deviation of pixel values
        contrast = np.std(gray) / 128  # Normalize to ~0-1
        contrast_score = min(1.0, contrast)

        # Ink coverage: percentage of dark pixels
        dark_pixels = np.sum(gray < 128) / gray.size
        # Optimal is around 20-40%
        if dark_pixels < 0.05:
            coverage_score = dark_pixels / 0.05
        elif dark_pixels > 0.6:
            coverage_score = (1.0 - dark_pixels) / 0.4
        else:
            coverage_score = 1.0

        # Size: prefer larger images
        size_score = min(1.0, min(gray.shape) / 100)

        # Combine scores
        return 0.4 * contrast_score + 0.4 * coverage_score + 0.2 * size_score


def main():
    """Test the processor."""
    processor = GlyphImageProcessor()

    # Test with 道
    images = processor.list_glyph_images("道")
    print(f"Found {len(images)} images for 道")

    if images:
        # Process first image
        result = processor.process_for_tracing(images[0])
        print(f"Processing result: success={result['success']}")
        if result['success']:
            print(f"  Original size: {result['metadata']['original_size']}")
            print(f"  Processed size: {result['metadata']['processed_size']}")

            # Quality score
            score = processor.get_image_quality_score(images[0])
            print(f"  Quality score: {score:.2f}")


if __name__ == "__main__":
    main()
