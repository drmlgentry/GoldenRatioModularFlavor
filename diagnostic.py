# diagnostic.py
import numpy as np

# Golden ratio
phi = (1 + np.sqrt(5)) / 2
print(f"Golden ratio φ = {phi:.10f}")
print(f"φ⁻¹ = {1/phi:.10f}")
print(f"φ⁻² = {1/phi**2:.10f}")

print("\n" + "="*60)

# Your M₀ matrix from the output
M0 = np.array([
    [-1.15470054, -0.57735027, -0.61803399],
    [-0.57735027,  0.71364418, -0.38196601],
    [-0.61803399, -0.38196601,  0.44105636]
])

print("1. YOUR M₀ MATRIX:")
print(M0)

print("\n2. EIGENVALUES:")
eigvals = np.linalg.eigvals(M0)
print(f"   λ₁ = {eigvals[0]:.6f}")
print(f"   λ₂ = {eigvals[1]:.6f}")
print(f"   λ₃ = {eigvals[2]:.6f}")

print("\n3. PAPER'S CLAIMED EIGENVALUES:")
paper_eigvals = np.array([-1.457, 0.382, 0.236])
print(f"   λ₁ = {paper_eigvals[0]:.6f}")
print(f"   λ₂ = {paper_eigvals[1]:.6f}")
print(f"   λ₃ = {paper_eigvals[2]:.6f}")

print("\n4. RATIO COMPARISON:")
print("   Your ratios (normalized to |λ₁|=1):")
your_ratios = np.abs(eigvals) / np.max(np.abs(eigvals))
print(f"   {your_ratios[0]:.3f} : {your_ratios[1]:.3f} : {your_ratios[2]:.3f}")

print("\n   Paper ratios (normalized to |λ₁|=1):")
paper_ratios = np.abs(paper_eigvals) / np.max(np.abs(paper_eigvals))
print(f"   {paper_ratios[0]:.3f} : {paper_ratios[1]:.3f} : {paper_ratios[2]:.3f}")

print("\n5. GOLDEN RATIO HIERARCHY CHECK:")
print(f"   Ideal: 1.000 : {1/phi:.3f} : {1/phi**2:.3f}")
print(f"   Your closeness to golden: {np.mean(np.abs(your_ratios - [1, 1/phi, 1/phi**2])):.4f}")
print(f"   Paper closeness to golden: {np.mean(np.abs(paper_ratios - [1, 1/phi, 1/phi**2])):.4f}")

print("\n" + "="*60)
print("CONCLUSION:")
if np.mean(np.abs(your_ratios - [1, 1/phi, 1/phi**2])) < 0.1:
    print("✓ YOUR eigenvalues follow the golden ratio hierarchy!")
else:
    print("✗ Something is off with the eigenvalues")