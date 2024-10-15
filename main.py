import math
import matplotlib.pyplot as plt
import numpy as np

# Period is the length of the wave
period = 6 * math.pi
# Length is the number of points in the x-axis
length = 1000
# Step is the distance between each point in the x-axis
step = period / length
# Define the sine wave
sin = [math.sin(x) for x in np.arange(0, period, step)]

# Create a figure and axis
figure, axis = plt.subplots(1,1)

# Plot the sine wave
axis.plot(sin)
axis.set_title('Sine Wave')
axis.set_xlabel('X')
axis.legend(['sin(x)'])
plt.show()