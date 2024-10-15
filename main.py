import math
import matplotlib.pyplot as plt
import numpy as np

# This function will be changed in the future
def generateDeviation(x):
    deviation = -6 * np.random.uniform(0, 1/math.sqrt(6)) + 1/math.sqrt(6)
    if deviation > 0.5:
        deviation *= -1
    return deviation

# Period is the length of the wave
period = 6 * math.pi
# Length is the number of points in the x-axis
length = 1000
# Step is the distance between each point in the x-axis
step = period / length
# Define the sine wave
sin = [math.sin(x) for x in np.arange(0, period, step)]

# Create a figure and axis
figure, axis = plt.subplots(2, 1)

# Plot the sine wave
axis[0].plot(sin)
axis[0].set_title('Sine Wave')
axis[0].set_xlabel('X')
axis[0].legend(['sin(x)'])

# Generate the deviation of the sine wave for every 10th point
deviation = [generateDeviation() if i % 10 == 0 else None for i in range(len(sin))]
deviation_points = [(i, deviation[i]) for i in range(len(deviation)) if deviation[i] is not None]

# Plot the deviation points as individual points
x_points = [point[0] for point in deviation_points]
y_points = [point[1] for point in deviation_points]
axis[1].plot(sin)
axis[1].plot(x_points, y_points, linestyle='none', marker='o', markersize=3, color='red')
axis[1].set_title('Sine Wave with Deviation')
axis[1].set_xlabel('X')
axis[1].legend(['sin(x) with Deviation'])

plt.tight_layout()
plt.show()