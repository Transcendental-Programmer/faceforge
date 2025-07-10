import numpy as np
from typing import Tuple, List, Optional
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

class LatentDirectionFinder:
    """
    Provides methods to discover semantic directions in latent space using PCA or classifier-based approaches.
    """
    def __init__(self, latent_vectors: np.ndarray):
        """
        :param latent_vectors: Array of shape (N, D) where N is the number of samples and D is the latent dimension.
        """
        self.latent_vectors = latent_vectors

    def pca_direction(self, n_components: int = 10) -> Tuple[np.ndarray, np.ndarray]:
        """
        Perform PCA on the latent vectors to find principal directions.
        :return: (components, explained_variance)
        """
        pca = PCA(n_components=n_components)
        pca.fit(self.latent_vectors)
        return pca.components_, pca.explained_variance_ratio_

    def classifier_direction(self, labels: List[int]) -> np.ndarray:
        """
        Fit a linear classifier to find a direction separating two classes in latent space.
        :param labels: List of 0/1 labels for each latent vector.
        :return: Normalized direction vector (D,)
        """
        clf = LogisticRegression()
        clf.fit(self.latent_vectors, labels)
        direction = clf.coef_[0]
        direction = direction / np.linalg.norm(direction)
        return direction 