import matplotlib.pyplot as plt
import numpy as np

# draw line between two points: A(1, 3); B(8, 10)

x_values = [1, 8]
y_values = [3, 10]

x_points = np.array(x_values)
y_points = np.array(y_values)

plt.plot(x_points, y_points, marker='o')
plt.show()

