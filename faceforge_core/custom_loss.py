import numpy as np
import torch
from typing import Callable

def attribute_preserving_loss(
    generated: torch.Tensor,
    original: torch.Tensor,
    attr_predictor: Callable[[torch.Tensor], torch.Tensor],
    y_target: torch.Tensor,
    lambda_pred: float = 1.0,
    lambda_recon: float = 1.0
) -> torch.Tensor:
    """
    Custom loss enforcing attribute fidelity and identity preservation.
    L_attr(G(z + alpha d)) = lambda_pred * ||f_attr(G(.)) - y_target||^2 + lambda_recon * ||G(z + alpha d) - G(z)||^2
    :param generated: Generated image tensor (B, ...)
    :param original: Original image tensor (B, ...)
    :param attr_predictor: Function mapping image tensor to attribute prediction
    :param y_target: Target attribute value tensor (B, ...)
    :param lambda_pred: Weight for attribute prediction loss
    :param lambda_recon: Weight for reconstruction loss
    :return: Scalar loss tensor
    """
    pred_loss = torch.nn.functional.mse_loss(attr_predictor(generated), y_target)
    recon_loss = torch.nn.functional.mse_loss(generated, original)
    return lambda_pred * pred_loss + lambda_recon * recon_loss 