import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point, Polygon, box, LineString
from matplotlib.patches import Polygon as PolygonPatch

def main():
    # create some example points
    point1 = Point(0, 0)
    point2 = Point(0, 0.5)
    point3 = Point(0.5, 0.5)
    point4 = Point(0.5, 0)
    point5 = Point(0, 0)


    # create a polygon from the points
    polygon = Polygon([point1, point5, point2, point3, point4])

    # create a LineString
    line = LineString([(1.2, 1.0999999999999999), (0.7, 1.0999999999999999)])
    line2 = LineString([(1, 2), (1, 1)])

    # check if line is contained in the polygon
    contained = line2.intersects(line)

    # print result
    print(contained)

    # extract x and y coordinates of polygon exterior
    xy = np.array(polygon.exterior.coords)

    # create a matplotlib figure and axis
    fig, ax = plt.subplots()

    # create a patch representing the polygon
    patch = PolygonPatch(xy, facecolor='blue', alpha=0.5)

    # add the patch to the axis
    ax.add_patch(patch)

    # create a line representing the LineString
    line_ax = LineString(line)
    ax.plot(*line_ax.xy, color='black')

    line_ax2 = LineString(line2)
    ax.plot(*line_ax2.xy, color='black')

    # set the axis limits and display the plot
    ax.set_xlim(-1, 2)
    ax.set_ylim(-1, 2)
    plt.show()

if __name__ == "__main__":
    main()