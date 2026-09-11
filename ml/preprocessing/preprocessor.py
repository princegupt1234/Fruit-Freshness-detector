import os
from pathlib import Path
from typing import Dict, Tuple

from PIL import Image
import numpy as np


class DatasetPreprocessor:
    def __init__(self, img_size: Tuple[int, int] = (224, 224), image_color_mode: str = "RGB"):
        self.img_size = img_size
        self.image_color_mode = image_color_mode

    def load_image(self, image_path: str | Path):
        img = Image.open(str(image_path)).convert(self.image_color_mode)
        img = img.resize(self.img_size)
        return np.asarray(img, dtype=np.float32) / 255.0

    def validate_path(self, image_path: str | Path) -> bool:
        path = Path(image_path)
        return path.exists() and path.is_file()


if __name__ == "__main__":
    preprocessor = DatasetPreprocessor()
    print("Preprocessor initialized with image size:", preprocessor.img_size)
