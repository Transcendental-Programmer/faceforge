import numpy as np
from typing import List, Optional, Tuple

class LatentPoint:
    """
    Represents a point in latent space with an associated prompt and encoding.
    """
    def __init__(self, text: str, encoding: Optional[np.ndarray], xy_pos: Optional[Tuple[float, float]] = None):
        self.text = text
        self.encoding = encoding
        self.xy_pos = xy_pos if xy_pos is not None else (0.0, 0.0)

    def move(self, new_xy_pos: Tuple[float, float]):
        self.xy_pos = new_xy_pos

class LatentSpaceExplorer:
    """
    Core logic for managing points in latent space and sampling new points.
    """
    def __init__(self):
        self.points: List[LatentPoint] = []
        self.selected_point_idx: Optional[int] = None

    def add_point(self, text: str, encoding: Optional[np.ndarray], xy_pos: Optional[Tuple[float, float]] = None):
        self.points.append(LatentPoint(text, encoding, xy_pos))

    def delete_point(self, idx: int):
        if 0 <= idx < len(self.points):
            del self.points[idx]

    def modify_point(self, idx: int, new_text: str, new_encoding: Optional[np.ndarray]):
        if 0 <= idx < len(self.points):
            self.points[idx].text = new_text
            self.points[idx].encoding = new_encoding

    def get_encodings(self) -> List[Optional[np.ndarray]]:
        return [p.encoding for p in self.points]

    def get_prompts(self) -> List[str]:
        return [p.text for p in self.points]

    def get_positions(self) -> np.ndarray:
        return np.array([p.xy_pos for p in self.points])

    def sample_encoding(self, point: Tuple[float, float], mode: str = "distance") -> Optional[np.ndarray]:
        """
        Sample a new encoding based on the given point and mode.
        """
        encodings = self.get_encodings()
        positions = self.get_positions()
        if not encodings or len(encodings) == 0:
            return None
        if mode == "distance":
            dists = np.linalg.norm(positions - np.array(point), axis=1)
            coefs = 1.0 / (1.0 + dists ** 2)
        elif mode == "circle":
            point_vec = np.array(point)
            positions_vec = positions
            coefs = np.dot(positions_vec, point_vec)
        else:
            raise ValueError(f"Unknown sampling mode: {mode}")
        coefs = coefs / np.sum(coefs)
        # Weighted sum of encodings
        result = None
        for coef, enc in zip(coefs, encodings):
            if enc is not None:
                if result is None:
                    result = coef * enc
                else:
                    result += coef * enc
        return result 