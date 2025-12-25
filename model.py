"""
Golden Ratio Modular Flavor Model - Corrected Implementation
Core calculations for the paper "The Golden Point in A5 Modular Flavor Symmetry"
"""

import numpy as np
from typing import Tuple

class GoldenRatioFlavorModel:
    """Implementation of the A5 modular flavor model at τ = exp(2πi/5)"""
    
    def __init__(self):
        self.phi = (1 + np.sqrt(5)) / 2  # Golden ratio
        self.phi_inv = 1 / self.phi
        self.phi_sq_inv = 1 / (self.phi**2)
        self.sqrt3 = np.sqrt(3)
        
    def modular_forms_at_tau0(self) -> np.ndarray:
        """Return the weight-2 modular forms Y_a(τ₀) from Theorem 2.1"""
        # Theorem 2.1: (Y₁, Y₂, Y₃, Y₄, Y₅) ∝ (1, φ⁻¹, φ⁻², -φ⁻², -φ⁻¹)
        # We normalize so Y₁ = 1
        return np.array([
            1.0,
            self.phi_inv,
            self.phi_sq_inv,
            -self.phi_sq_inv,
            -self.phi_inv
        ])
    
    def golden_matrix_M0(self) -> np.ndarray:
        """Construct the universal golden matrix from Eq. (3.2)"""
        Y = self.modular_forms_at_tau0()
        
        # Eq. (3.1): M_ij from Clebsch-Gordan coefficients
        M = np.array([
            [-2/self.sqrt3 * Y[0], -1/self.sqrt3 * (Y[3] + Y[4]), Y[4]],
            [-1/self.sqrt3 * (Y[3] + Y[4]), 2/self.sqrt3 * Y[1], Y[3]],
            [Y[4], Y[3], 2/self.sqrt3 * Y[2]]
        ])
        
        return M
    
    def yukawa_with_weights(self, weights: Tuple[int, int, int], 
                           overall_coupling: float = 1.0) -> np.ndarray:
        """
        Calculate Yukawa matrix with modular weight suppression.
        Eq. (4.2): Y_ij = g_F [M0]_ij φ^{-(k_i + k_j)/2}
        
        Args:
            weights: Tuple of modular weights (k1, k2, k3)
            overall_coupling: Overall coupling constant g_F
        """
        M0 = self.golden_matrix_M0()
        k = np.array(weights)
        
        # Create suppression matrix: φ^{-(k_i + k_j)/2}
        suppression = np.zeros((3, 3))
        for i in range(3):
            for j in range(3):
                suppression[i, j] = self.phi ** (-(k[i] + k[j]) / 2)
        
        return overall_coupling * M0 * suppression
    
    def neutrino_mass_matrix(self) -> np.ndarray:
        """
        Calculate neutrino mass matrix from Weinberg operator.
        M_ν ∝ M0^2 (up to overall scale)
        """
        M0 = self.golden_matrix_M0()
        return np.dot(M0, M0)  # M0 squared
    
    def analyze_hierarchy(self, weights: Tuple[int, int, int] = (6, 4, 0)) -> dict:
        """Analyze hierarchical structure for given modular weights"""
        M0 = self.golden_matrix_M0()
        Y = self.yukawa_with_weights(weights)
        M_nu = self.neutrino_mass_matrix()
        
        # Eigenvalues
        eig_M0 = np.linalg.eigvals(M0)
        eig_Y = np.linalg.eigvals(Y)
        eig_nu = np.linalg.eigvals(M_nu)
        
        return {
            'M0_eigenvalues': np.sort(np.abs(eig_M0))[::-1],
            'Yukawa_eigenvalues': np.sort(np.abs(eig_Y))[::-1],
            'Neutrino_eigenvalues': np.sort(np.abs(eig_nu))[::-1],
            'mass_ratios': {
                'M0': np.sort(np.abs(eig_M0))[::-1] / np.max(np.abs(eig_M0)),
                'Yukawa': np.sort(np.abs(eig_Y))[::-1] / np.max(np.abs(eig_Y)),
                'Neutrino': np.sort(np.abs(eig_nu))[::-1] / np.max(np.abs(eig_nu))
            }
        }
    
    def verify_golden_relations(self) -> dict:
        """Verify key mathematical relations from the paper"""
        Y = self.modular_forms_at_tau0()
        M0 = self.golden_matrix_M0()
        
        results = {}
        
        # 1. Verify Y₄ + Y₅ = -1 (Corollary 2.2)
        results['Y4_plus_Y5'] = Y[3] + Y[4]
        results['Y4_plus_Y5_expected'] = -1.0
        
        # 2. Verify φ relations
        results['phi_relation'] = self.phi**2 - self.phi - 1
        
        # 3. Check matrix properties
        results['is_symmetric'] = np.allclose(M0, M0.T)
        results['M0_trace'] = np.trace(M0)
        
        # 4. Eigenvalue scaling
        eigvals = np.linalg.eigvals(M0)
        sorted_eig = np.sort(np.abs(eigvals))[::-1]
        if len(sorted_eig) >= 3:
            results['eigenvalue_ratio_12'] = sorted_eig[1] / sorted_eig[0]
            results['eigenvalue_ratio_23'] = sorted_eig[2] / sorted_eig[1]
            results['phi_inv'] = self.phi_inv
        
        return results
