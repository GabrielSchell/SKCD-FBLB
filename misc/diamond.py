import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create a figure and axis
fig, ax = plt.subplots()

ax.axis('off')
# Define the coordinates for the vertices of the diamond
diamond_coords = [(0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5)]

# Create a polygon patch for the diamond
diamond_patch_b = patches.Polygon(diamond_coords, closed=True, facecolor='#51acc9', edgecolor='black', linewidth=20)
diamond_patch_w = patches.Polygon(diamond_coords, closed=True, facecolor='white', edgecolor='black', linewidth=20)

# Add the diamond patch to the axis
ax.add_patch(diamond_patch_b)
# Set axis limits and remove axis labels and ticks
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')  # Make the aspect ratio equal to create a diamond shape

fig.savefig('temp.png', transparent=True)


ax.add_patch(diamond_patch_w)
# Set axis limits and remove axis labels and ticks
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_aspect('equal')  # Make the aspect ratio equal to create a diamond shape

# Display the plot
#plt.show()

fig.savefig('temp2.png', transparent=True)