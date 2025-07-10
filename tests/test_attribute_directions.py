import unittest
import numpy as np
from faceforge_core.attribute_directions import LatentDirectionFinder

class TestLatentDirectionFinder(unittest.TestCase):
    def setUp(self):
        # 100 samples, 5D latent
        self.latents = np.random.randn(100, 5)
        self.labels = [0]*50 + [1]*50
        self.finder = LatentDirectionFinder(self.latents)

    def test_pca_direction(self):
        components, explained = self.finder.pca_direction(n_components=2)
        self.assertEqual(components.shape, (2, 5))
        self.assertEqual(explained.shape, (2,))

    def test_classifier_direction(self):
        direction = self.finder.classifier_direction(self.labels)
        self.assertEqual(direction.shape, (5,))
        self.assertAlmostEqual(np.linalg.norm(direction), 1.0, places=5)

if __name__ == "__main__":
    unittest.main() 