import unittest
import torch
from faceforge_core.custom_loss import attribute_preserving_loss

class TestAttributePreservingLoss(unittest.TestCase):
    def setUp(self):
        self.generated = torch.ones((2, 3, 4, 4))
        self.original = torch.zeros((2, 3, 4, 4))
        self.y_target = torch.ones((2, 1))
        self.attr_predictor = lambda x: torch.ones((2, 1))

    def test_loss_value(self):
        loss = attribute_preserving_loss(
            self.generated, self.original, self.attr_predictor, self.y_target, lambda_pred=2.0, lambda_recon=3.0
        )
        # pred_loss = 0, recon_loss = mean((1-0)^2) = 1
        self.assertAlmostEqual(loss.item(), 3.0)

    def test_loss_with_nonzero_pred(self):
        attr_predictor = lambda x: torch.zeros((2, 1))
        loss = attribute_preserving_loss(
            self.generated, self.original, attr_predictor, self.y_target, lambda_pred=2.0, lambda_recon=3.0
        )
        # pred_loss = mean((0-1)^2) = 1, recon_loss = 1
        self.assertAlmostEqual(loss.item(), 5.0)

if __name__ == "__main__":
    unittest.main() 