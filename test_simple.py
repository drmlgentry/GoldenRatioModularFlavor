import numpy as np 
phi = (1 + 5**0.5)/2 
print("Testing Table 2 mystery") 
print("Golden ratio =", phi) 
M0 = [[-1.1547, -0.57735, -0.618034], [-0.57735, 0.713644, -0.381966], [-0.618034, -0.381966, 0.441056]] 
k = [6, 4, 0] 
import numpy as np 
S = np.zeros((3,3)) 
for i in range(3): 
    for j in range(3): 
        S[i,j] = phi**(-(k[i]+k[j])/2) 
Y = M0 * S 
eig = np.linalg.eigvals(Y) 
ratios = abs(eig) / max(abs(eig)) 
print("Ratios:", ratios[0], ":", ratios[1], ":", ratios[2]) 
