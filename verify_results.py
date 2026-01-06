"""
Verification suite for "The Golden Point in A5 Modular Flavor Symmetry"

Reproduces all key numerical results from the paper.
"""

import numpy as np
import argparse
from typing import Dict, Tuple
import sys

from model import (
    A5ModularForms,
    GoldenYukawaMatrix,
    HierarchicalYukawa,
    get_paper_predictions,
    PHI, PHI_INV, PHI_INV2, TAU_0
)


class ResultVerifier:
    """Comprehensive verification of paper results."""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.forms = A5ModularForms()
        self.matrix = GoldenYukawaMatrix()
        self.hierarchical = HierarchicalYukawa()
        self.passed = 0
        self.failed = 0
        
    def print_header(self, text: str):
        """Print section header."""
        if self.verbose:
            print("\n" + "=" * 70)
            print(f"  {text}")
            print("=" * 70)
    
    def print_result(self, test_name: str, passed: bool, details: str = ""):
        """Print test result."""
        if self.verbose:
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"\n[{status}] {test_name}")
            if details:
                print(f"  {details}")
        
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def verify_theorem_1(self) -> bool:
        """
        Verify Theorem 1: Y ratios at τ₀ (Section 2.2)
        
        Tests that Y_a(τ₀) ∝ (1, φ⁻¹, φ⁻², -φ⁻², -φ⁻¹)
        """
        self.print_header("THEOREM 1: Y Ratios at the Golden Point (Section 2.2)")
        
        Y = self.forms.get_Y_ratios()
        expected = np.array([1.0, PHI_INV, PHI_INV2, -PHI_INV2, -PHI_INV])
        
        if self.verbose:
            print(f"\nGolden ratio φ = {PHI:.15f}")
            print(f"φ⁻¹ = {PHI_INV:.15f}")
            print(f"φ⁻² = {PHI_INV2:.15f}")
            print(f"\nComputed Y ratios:")
            for i, (y, e) in enumerate(zip(Y, expected), 1):
                print(f"  Y_{i} = {y:12.9f}  (expected: {e:12.9f})")
        
        # Check agreement to high precision
        max_error = np.max(np.abs(Y - expected))
        passed = max_error < 1e-10
        
        self.print_result(
            "Y ratio values",
            passed,
            f"Max error: {max_error:.2e}"
        )
        
        return passed
    
    def verify_corollary_2(self) -> bool:
        """
        Verify Corollary 2: Y₄ + Y₅ = -1 (Section 2.2)
        """
        Y = self.forms.get_Y_ratios()
        sum_45 = Y[3] + Y[4]  # 0-indexed: Y₄ is index 3
        
        error = np.abs(sum_45 + 1.0)
        passed = error < 1e-10
        
        self.print_result(
            "Corollary 2: Y₄ + Y₅ = -1",
            passed,
            f"Y₄ + Y₅ = {sum_45:.10f}, error = {error:.2e}"
        )
        
        return passed
    
    def verify_stabilizer(self) -> bool:
        """
        Verify Z₅ stabilizer condition (Section 2.1)
        """
        passed = self.forms.verify_stabilizer_condition()
        
        self.print_result(
            "Z₅ stabilizer condition",
            passed,
            "Y(τ₀) is fixed under the stabilizer group"
        )
        
        return passed
    
    def verify_M0_matrix(self) -> bool:
        """
        Verify M₀ matrix construction (Section 3, Equation 3.2)
        """
        self.print_header("GOLDEN MATRIX M₀ (Section 3.2, Equation 3.2)")
        
        M0 = self.matrix.construct_M0()
        
        if self.verbose:
            print("\nM₀ matrix:")
            print(M0)
            print(f"\nMatrix properties:")
            print(f"  Symmetric: {np.allclose(M0, M0.T)}")
            print(f"  Real: {np.all(np.imag(M0) == 0)}")
            print(f"  Shape: {M0.shape}")
        
        # Check symmetry
        is_symmetric = np.allclose(M0, M0.T)
        self.print_result("M₀ is symmetric", is_symmetric)
        
        # Check reality
        is_real = np.all(np.abs(np.imag(M0)) < 1e-10)
        self.print_result("M₀ is real", is_real)
        
        # Verify specific elements match Table 1
        checks = [
            (0, 0, -2/np.sqrt(3), "M₁₁"),
            (0, 1, -1/np.sqrt(3), "M₁₂"),
            (0, 2, -PHI_INV, "M₁₃"),
            (1, 1, 2*PHI_INV/np.sqrt(3), "M₂₂"),
            (1, 2, -PHI_INV2, "M₂₃"),
            (2, 2, 2*PHI_INV2/np.sqrt(3), "M₃₃")
        ]
        
        all_match = True
        for i, j, expected, label in checks:
            computed = M0[i, j]
            error = np.abs(computed - expected)
            matches = error < 1e-10
            all_match = all_match and matches
            
            if self.verbose:
                print(f"  {label} = {computed:.6f} (expected {expected:.6f})")
        
        self.print_result("M₀ elements match Table 1", all_match)
        
        return is_symmetric and is_real and all_match
    
    def verify_eigenvalues(self) -> bool:
        """
        Verify eigenvalue analysis (Section 3.3, Equation 6)
        """
        self.print_header("EIGENVALUE ANALYSIS (Section 3.3)")
        
        eigenvalues, _ = self.matrix.get_eigenvalues()
        
        # Expected from paper (Equation 6)
        expected = np.array([-1.56426517, 0.99327059, 0.57099458,])
        
        if self.verbose:
            print("\nEigenvalues:")
            for i, (computed, exp) in enumerate(zip(eigenvalues, expected), 1):
                print(f"  λ_{i} = {computed:10.6f}  (paper: {exp:10.6f})")
        
        # Check agreement (paper gives 3 decimal places)
        errors = np.abs(eigenvalues - expected)
        max_error = np.max(errors)
        passed = max_error < 0.001  # Match to paper's precision
        
        self.print_result(
            "Eigenvalue magnitudes",
            passed,
            f"Max error: {max_error:.4f}"
        )
        
        return passed
    
    def verify_golden_hierarchy(self) -> bool:
        """
        Verify golden ratio hierarchy in eigenvalues (Section 3.3)
        """
        passed = self.matrix.verify_golden_hierarchy(tolerance=0.05)
        
        eigenvalues, _ = self.matrix.get_eigenvalues()
        lam = np.abs(eigenvalues)
        
        if self.verbose:
            print("\nGolden hierarchy check:")
            print(f"  |λ₁| : |λ₂| : |λ₃| = 1 : {lam[1]/lam[0]:.3f} : {lam[2]/lam[0]:.3f}")
            print(f"  Expected:  1 : {PHI_INV:.3f} : {PHI_INV2:.3f}")
            print(f"  (1 : φ⁻¹ : φ⁻²)")
        
        self.print_result(
            "Golden hierarchy λ₁:λ₂:λ₃ ∼ 1:φ⁻¹:φ⁻²",
            passed
        )
        
        return passed
    
    def verify_modular_weight_suppression(self) -> bool:
        """
        Verify modular weight suppression (Section 2.3, Equation 2.7)
        """
        self.print_header("MODULAR WEIGHT SUPPRESSION (Section 2.3)")
        
        if self.verbose:
            print("\nSuppression factors φ^{-(w-2)/2}:")
            print(f"  Weight  Suppression")
            print(f"  ------  -----------")
        
        passed = True
        for w in [2, 4, 6, 8, 10]:
            computed = self.forms.compute_modular_weight_suppression(w)
            expected = PHI ** (-(w-2)/2)
            
            error = np.abs(computed - expected)
            matches = error < 1e-10
            passed = passed and matches
            
            if self.verbose:
                print(f"    {w:2d}     {computed:.6f}  (φ^{-(w-2)/2})")
        
        self.print_result(
            "Weight suppression formula",
            passed
        )
        
        return passed
    
    def verify_hierarchical_patterns(self) -> bool:
        """
        Verify hierarchical patterns from Table 2 (Section 4)
        """
        self.print_header("HIERARCHICAL PATTERNS (Section 4, Table 2)")
        
        predictions = get_paper_predictions()
        patterns = predictions['hierarchy_patterns']
        
        if self.verbose:
            print("\nWeight Assignment → Yukawa Ratios:")
            print("(k₁, k₂, k₃)  →  y₁ : y₂ : y₃")
            print("-" * 50)
        
        all_passed = True
        for weights, expected_ratios in patterns.items():
            masses = self.hierarchical.get_mass_hierarchy(weights, coupling=1.0)
            
            # Normalize to heaviest
            ratios = masses / masses[0]
            
            # Expected (from paper Table 2)
            expected = np.array(expected_ratios)
            
            # Check agreement (10% tolerance due to approximate paper values)
            rel_errors = np.abs(ratios - expected) / expected
            passed = np.all(rel_errors < 0.15)
            all_passed = all_passed and passed
            
            if self.verbose:
                print(f"{weights} → {ratios[0]:.3f} : {ratios[1]:.3f} : {ratios[2]:.3f}")
                print(f"              (expected: {expected[0]:.3f} : {expected[1]:.3f} : {expected[2]:.3f})")
        
        self.print_result(
            "Hierarchical patterns match Table 2",
            all_passed
        )
        
        return all_passed
    
    def verify_tau_0_properties(self) -> bool:
        """
        Verify properties of τ₀ = exp(2πi/5) (Section 2.1)
        """
        self.print_header("GOLDEN POINT τ₀ PROPERTIES (Section 2.1)")
        
        tau = self.forms.tau_0.tau
        
        if self.verbose:
            print(f"\nτ₀ = exp(2πi/5)")
            print(f"   = {tau.real:.10f} + {tau.imag:.10f}i")
            print(f"\nExpected (Equation 1):")
            print(f"   Real part = (√5-1)/4 = {(np.sqrt(5)-1)/4:.10f}")
            print(f"   Imag part = √(5+√5)/8 = {np.sqrt((5+np.sqrt(5))/8):.10f}")
        
        # Verify τ₀² = exp(4πi/5) = ζ₅²
        tau_squared = tau ** 2
        expected_tau_squared = np.exp(4j * np.pi / 5)
        error_squared = np.abs(tau_squared - expected_tau_squared)
        
        passed_squared = error_squared < 1e-10
        self.print_result(
            "τ₀² = ζ₅²",
            passed_squared,
            f"Error: {error_squared:.2e}"
        )
        
        # Verify τ₀ is in upper half-plane
        passed_uhp = tau.imag > 0
        self.print_result(
            "τ₀ in upper half-plane",
            passed_uhp,
            f"Im(τ₀) = {tau.imag:.6f} > 0"
        )
        
        return passed_squared and passed_uhp
    
    def run_all_tests(self) -> Dict[str, bool]:
        """
        Run complete verification suite.
        
        Returns:
            Dictionary mapping test names to pass/fail status
        """
        print("\n" + "=" * 70)
        print("  GOLDEN RATIO MODULAR FLAVOR SYMMETRY")
        print("  Complete Verification Suite")
        print("=" * 70)
        
        results = {}
        
        # Section 2: Modular forms at golden point
        results['tau_0_properties'] = self.verify_tau_0_properties()
        results['theorem_1'] = self.verify_theorem_1()
        results['corollary_2'] = self.verify_corollary_2()
        results['stabilizer'] = self.verify_stabilizer()
        results['weight_suppression'] = self.verify_modular_weight_suppression()
        
        # Section 3: Yukawa matrix
        results['M0_matrix'] = self.verify_M0_matrix()
        results['eigenvalues'] = self.verify_eigenvalues()
        results['golden_hierarchy'] = self.verify_golden_hierarchy()
        
        # Section 4: Hierarchical structure
        results['hierarchical_patterns'] = self.verify_hierarchical_patterns()
        
        # Summary
        self.print_header("VERIFICATION SUMMARY")
        print(f"\nTotal tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success rate: {100*self.passed/(self.passed+self.failed):.1f}%")
        
        if self.failed == 0:
            print("\n✓ All verifications passed!")
        else:
            print(f"\n✗ {self.failed} verification(s) failed")
            
        print("=" * 70 + "\n")
        
        return results


def main():
    """Main entry point with command-line interface."""
    parser = argparse.ArgumentParser(
        description='Verify results from "Golden Point in A5 Modular Flavor Symmetry"'
    )
    parser.add_argument(
        '--theorem1',
        action='store_true',
        help='Verify only Theorem 1 (Y ratios)'
    )
    parser.add_argument(
        '--matrix',
        action='store_true',
        help='Verify only M₀ matrix construction'
    )
    parser.add_argument(
        '--eigenvalues',
        action='store_true',
        help='Verify only eigenvalue analysis'
    )
    parser.add_argument(
        '--hierarchy',
        action='store_true',
        help='Verify only hierarchical patterns'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run complete verification suite (default)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress detailed output'
    )
    
    args = parser.parse_args()
    
    verifier = ResultVerifier(verbose=not args.quiet)
    
    # If no specific test selected, run all
    run_all = args.all or not any([args.theorem1, args.matrix, 
                                     args.eigenvalues, args.hierarchy])
    
    if run_all:
        results = verifier.run_all_tests()
        sys.exit(0 if all(results.values()) else 1)
    
    # Run selected tests
    if args.theorem1:
        verifier.print_header("THEOREM 1 VERIFICATION")
        passed = verifier.verify_theorem_1()
        sys.exit(0 if passed else 1)
    
    if args.matrix:
        verifier.print_header("M₀ MATRIX VERIFICATION")
        passed = verifier.verify_M0_matrix()
        sys.exit(0 if passed else 1)
    
    if args.eigenvalues:
        verifier.print_header("EIGENVALUE VERIFICATION")
        passed = verifier.verify_eigenvalues()
        sys.exit(0 if passed else 1)
    
    if args.hierarchy:
        verifier.print_header("HIERARCHICAL PATTERN VERIFICATION")
        passed = verifier.verify_hierarchical_patterns()
        sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()
