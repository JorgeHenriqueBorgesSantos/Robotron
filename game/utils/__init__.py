from typing import Tuple
import numpy as np


def crop(image: np.ndarray, dims: Tuple[int, int, int, int]) -> np.ndarray:

    left, top, right, bottom = dims
    return image[left:right, top:bottom]
