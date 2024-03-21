import numpy as np
x = [1,2,3,4,5,6,7,8,9]
minimum = min(x)
maximum = max(x)
for i in range(len(x)):
    x[i] = ((x[i] - minimum) / (maximum - minimum)) * 2 - 1
print(x)