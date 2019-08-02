import numpy as np
import bezier
import matplotlib
from matplotlib import pyplot as plt


# Shooting example
# car at 0.0, facing left (-1, 0)
# ball at (2, 2)
# hit ball toward net - right (1, 0)
# coordinates description:
    # 1. car position
    # 2. position in front of car
    # 3. position in front of ball and net
    # 4. position just in front of ball and net (closer)
    # 5. ball position

nodes = np.asfortranarray([
    # [-283.59, -86.56, 1209.98, 1152.66, 1114.44],
    # [1296.07, 1261.8, 1091.04, 796.78, 600.61],
    [0.0, 1.4, 2.0],
    [0.0, 2.0, 2.0],
])

curve = bezier.Curve(nodes, degree=10)
curve.plot(256)

next_coordinate = curve.evaluate(0.2)
print(next_coordinate)

plt.show()
