import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["font.size"] = 10

plt.figure(figsize=(5,3))
plt.plot(np.sin(np.sinc(np.arange(0,10,0.001))), 'r', lw=2)

plt.show()