# eigenvalue_test.py 
import numpy as np 
 
# Your M0 matrix 
M0 = np.array([ 
    [-1.15470054, -0.57735027, -0.61803399], 
    [-0.57735027,  0.71364418, -0.38196601], 
    [-0.61803399, -0.38196601,  0.44105636] 
]) 
 
# Golden ratio 
phi = (1 + np.sqrt(5)) / 2 
 
print("="*70) 
print("MATHEMATICAL CONSISTENCY CHECK") 
print("="*70) 
