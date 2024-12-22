import matplotlib.pyplot as plt
import numpy as np

# Create a figure and 3D axis
fig = plt.figure()
ax = plt.axes(projection='3d')

# Generate data
x = np.arange(-5, 5, 1)
y = np.arange(-5, 5, 1)
x, y = np.meshgrid(x, y)
z = x**2 + y**2

# Plot the surface
surf = ax.plot_surface(x, y, z, cmap=plt.cm.cool)  # Corrected 'camp' to 'cmap'

# Set titles and labels
ax.set_title("3D Plot")
ax.set_xlabel("X")  # Corrected 'set_xlable' to 'set_xlabel'
ax.set_ylabel("Y")  # Corrected 'set_ylable' to 'set_ylabel'
ax.set_zlabel("Z")  # Corrected 'set_zlable' to 'set_zlabel'

# Add a colorbar
fig.colorbar(surf, location="left")

# Show the plot
plt.show()
