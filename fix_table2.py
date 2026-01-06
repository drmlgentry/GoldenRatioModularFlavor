with open('model.py', 'r') as f: 
    text = f.read() 
text = text.replace('[1.000, 0.146, 0.024]', '[1.000, 0.267, 0.191]') 
text = text.replace('[1.000, 0.055, 0.024]', '[1.000, 0.161, 0.132]') 
text = text.replace('[1.000, 0.021, 0.024]', '[1.000, 0.069, 0.058]') 
text = text.replace('[1.000, 0.382, 0.146]', '[1.000, 0.518, 0.388]') 
with open('model.py', 'w') as f: 
    f.write(text) 
print('Fixed! Table 2 values updated to match your computation') 
