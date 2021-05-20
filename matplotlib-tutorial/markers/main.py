import matplotlib.pyplot as plt
import numpy as np

x_points = np.array([1, 3])
y_points = np.array([8, 10])

plt.plot(x_points, y_points, 'o-r', ms=20, mec='cyan', mfc='hotpink')
plt.show()