#!/usr/bin/env python
"""
Quick installation and sanity check for Golden Ratio Modular Flavor code.

Run this after installation to verify everything works.
"""

import sys

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    try:
        import numpy
        print("  ✓ numpy")
    except ImportError as e:
        print(f"  ✗ numpy: {e}")
        return False
    
    try:
        import scipy
        print("  ✓ scipy")
    except ImportError as e:
        print(f"  ✗ scipy: {e}")
        return False
    
    try:
        import matplotlib
        print("  ✓ matplotlib")
    except ImportError as e:
        print(f"  ✗ matplotlib: {e}")
        return False
    
    try:
        from model import A5ModularForms, GoldenYukawaMatrix, HierarchicalYukawa
        print("  ✓ model module")
    except ImportError as e:
        print(f"  ✗ model module: {e}")
        return False
    
    return True


def test_basic_functionality():
    """Test basic functionality of the code."""
    print("\nTesting basic functionality...")
    
    try:
        from model import A5ModularForms, PHI, PHI_INV
        import numpy as np
        
        # Test 1: Golden ratio
        if abs(PHI - 1.618033988749895) < 1e-10:
            print("  ✓ Golden ratio φ correct")
        else:
            print("  ✗ Golden ratio φ incorrect")
            return False
        
        # Test 2: Y ratios
        forms = A5ModularForms()
        Y = forms.get_Y_ratios()
        expected = np.array([1.0, PHI_INV, PHI_INV**2, -PHI_INV**2, -PHI_INV])
        if np.max(np.abs(Y - expected)) < 1e-10:
            print("  ✓ Y ratios computed correctly")
        else:
            print("  ✗ Y ratios incorrect")
            return False
        
        # Test 3: M₀ matrix
        from model import GoldenYukawaMatrix
        matrix = GoldenYukawaMatrix()
        M0 = matrix.construct_M0()
        if M0.shape == (3, 3) and np.allclose(M0, M0.T):
            print("  ✓ M₀ matrix constructed (3×3, symmetric)")
        else:
            print("  ✗ M₀ matrix construction failed")
            return False
        
        # Test 4: Eigenvalues
        eigenvalues, _ = matrix.get_eigenvalues()
        if len(eigenvalues) == 3:
            print(f"  ✓ Eigenvalues computed: {eigenvalues}")
        else:
            print("  ✗ Eigenvalue computation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_verification_script():
    """Test that the verification script can be imported."""
    print("\nTesting verification script...")
    try:
        from verify_results import ResultVerifier
        print("  ✓ verify_results module imports successfully")
        
        # Try to create verifier (but don't run full suite)
        verifier = ResultVerifier(verbose=False)
        print("  ✓ ResultVerifier instantiated")
        
        return True
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def main():
    """Run all tests."""
    print("="*70)
    print("  Golden Ratio Modular Flavor - Installation Test")
    print("="*70)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
        print("\n✗ Import test FAILED")
        print("\nPlease install missing dependencies:")
        print("  pip install -r requirements.txt")
    else:
        print("\n✓ Import test PASSED")
    
    # Test basic functionality (only if imports passed)
    if all_passed:
        if not test_basic_functionality():
            all_passed = False
            print("\n✗ Functionality test FAILED")
        else:
            print("\n✓ Functionality test PASSED")
    
    # Test verification script
    if all_passed:
        if not test_verification_script():
            all_passed = False
            print("\n✗ Verification script test FAILED")
        else:
            print("\n✓ Verification script test PASSED")
    
    # Final summary
    print("\n" + "="*70)
    if all_passed:
        print("  ✓ ALL TESTS PASSED")
        print("\nInstallation successful! You can now:")
        print("  1. Run full verification: python verify_results.py")
        print("  2. Open demo notebook: jupyter notebook demo.ipynb")
        print("  3. Import and use the model: from model import A5ModularForms")
    else:
        print("  ✗ SOME TESTS FAILED")
        print("\nPlease check the errors above and:")
        print("  1. Install missing dependencies: pip install -r requirements.txt")
        print("  2. Verify Python version >= 3.8: python --version")
        print("  3. Check for error messages above")
    print("="*70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
