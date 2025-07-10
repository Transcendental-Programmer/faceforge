import unittest
import numpy as np
from faceforge_core.latent_explorer import LatentSpaceExplorer, LatentPoint

class TestLatentSpaceExplorer(unittest.TestCase):
    def setUp(self):
        self.explorer = LatentSpaceExplorer()
        self.dummy_encoding = np.array([1.0, 2.0])

    def test_add_point(self):
        self.explorer.add_point("test", self.dummy_encoding, (0.5, 0.5))
        self.assertEqual(len(self.explorer.points), 1)
        self.assertEqual(self.explorer.points[0].text, "test")
        np.testing.assert_array_equal(self.explorer.points[0].encoding, self.dummy_encoding)
        self.assertEqual(self.explorer.points[0].xy_pos, (0.5, 0.5))

    def test_delete_point(self):
        self.explorer.add_point("test", self.dummy_encoding)
        self.explorer.delete_point(0)
        self.assertEqual(len(self.explorer.points), 0)

    def test_modify_point(self):
        self.explorer.add_point("test", self.dummy_encoding)
        new_encoding = np.array([3.0, 4.0])
        self.explorer.modify_point(0, "new", new_encoding)
        self.assertEqual(self.explorer.points[0].text, "new")
        np.testing.assert_array_equal(self.explorer.points[0].encoding, new_encoding)

    def test_sample_encoding_distance(self):
        self.explorer.add_point("a", np.array([1.0, 0.0]), (0.0, 0.0))
        self.explorer.add_point("b", np.array([0.0, 1.0]), (1.0, 0.0))
        sampled = self.explorer.sample_encoding((0.5, 0.0), mode="distance")
        self.assertIsNotNone(sampled)
        self.assertEqual(sampled.shape, (2,))

    def test_sample_encoding_circle(self):
        self.explorer.add_point("a", np.array([1.0, 0.0]), (1.0, 0.0))
        self.explorer.add_point("b", np.array([0.0, 1.0]), (0.0, 1.0))
        sampled = self.explorer.sample_encoding((1.0, 1.0), mode="circle")
        self.assertIsNotNone(sampled)
        self.assertEqual(sampled.shape, (2,))

if __name__ == "__main__":
    unittest.main() 