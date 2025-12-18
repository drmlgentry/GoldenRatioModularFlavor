"""
Core model implementation.
"""

import numpy as np

class GoldenRatioModel:
    def __init__(self):
        self.phi = (1 + np.sqrt(5)) / 2
        
    def get_golden_matrix(self):
        """Return the golden matrix M0"""
        return np.array([
            [2, 1, -np.sqrt(3)/self.phi],
            [1, 2/self.phi, -np.sqrt(3)/self.phi**2],
            [-np.sqrt(3)/self.phi, -np.sqrt(3)/self.phi**2, 2/self.phi**2]
        ]) / np.sqrt(3)
    
    def calculate_mixing_angle(self):
        """Calculate θ₁₂ from golden matrix"""
        M0 = self.get_golden_matrix()
        vals, vecs = np.linalg.eig(M0)
        v1 = vecs[:, 0]
        v2 = vecs[:, 1]
        cos_theta = np.abs(np.dot(v1, v2)) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return np.arccos(cos_theta)