import matplotlib.pyplot as plt
import numpy as np
x=np.linspace(0, 50, 50)
y=0.5*x**2+2*x+10+np.random.normal(0,20,50)
plt.scatter(x, y, color='black', label='ugly noise signal')
plt.legend()
plt.show()