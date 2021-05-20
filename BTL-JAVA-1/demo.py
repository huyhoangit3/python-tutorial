import matplotlib.pyplot as plt
import numpy as np


class Sensor:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index


s1 = Sensor(30, 50, 1)
s2 = Sensor(60, 20, 2)

xpoint = np.array([s1.x, s2.x])
ypoint = np.array([s1.y, s2.y])
labels = [s1.index, s2.index]

Drawing_uncolored_circle = plt.Circle((s1.x, s1.y),
                                      10,
                                      fill=False)
Drawing_uncolored_circle1 = plt.Circle((s2.x, s2.y),
                                       10,
                                       fill=False)
fig, ax = plt.subplots();
ax.scatter(xpoint, ypoint)
ax.set_aspect(1)
ax.add_artist(Drawing_uncolored_circle)
ax.add_artist(Drawing_uncolored_circle1)

for i, txt in enumerate(labels):
    ax.annotate(txt, (xpoint[i], ypoint[i]))

plt.plot(xpoint, ypoint, "o")
plt.plot(xpoint, ypoint)
plt.xlim([0, 100])
plt.ylim([0, 100])
plt.show()
