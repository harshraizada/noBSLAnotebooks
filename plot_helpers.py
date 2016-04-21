from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
import numpy as np

# Helper functions for plotting vectors, lines, and planes using matplotlib
#
# Design
# ------
# We want to have functions `plot_vec`, `plot_line`, `plot_plane` that are easy
# to use and can handle both 2D and 3D SymPy Matrix inputs. 

def plot_vec(vec, at=[0,0,0], color='k'):
    """
    Plot the 2d or 3d vector `vec`, which can be a SymPy Matrix, a numpy array,
    or a python list.
    """
    if len(vec) == 3:
        ax = plt.gca(projection='3d')
        ax.set_aspect("equal")
        vec_x = float(vec[0])
        vec_y = float(vec[1])
        vec_z = float(vec[2])
        a = Arrow3D([at[0], vec_x],
                    [at[1], vec_y],
                    [at[2], vec_z],
                    mutation_scale=20,
                    lw=1,
                    arrowstyle="-|>",
                    color=color)
        ax.add_artist(a)
    elif len(vec) == 2:
        ax = plt.gca()
        ax.set_aspect("equal")
        vec_x = float(vec[0])
        vec_y = float(vec[1])
        a = Arrow2D([at[0], vec_x],
                    [at[1], vec_y],
                    mutation_scale=20,
                    lw=1,
                    arrowstyle="-|>",
                    color=color)
        ax.add_artist(a)
    else:
        print('Error: plot_vec supports only 2D and 3D vectors.')


def plot_vecs(*args):
    """Plot each of the vectors in the arugment list in a different color."""
    COLORS = ['k', 'b', 'g', 'r', 'c', 'm']
    for i, vec in enumerate(args):
        plot_vec(vec, color=COLORS[i%len(COLORS)])


def plot_line(dir_vec, point, color=None):
    """
    Plots the line with direction vector `dir_vec` passing though `point`.
    """
    if len(dir_vec) == 3:
        ax = plt.gca(projection='3d')
        ax.set_aspect("equal")
        dir_vec_x = float(dir_vec[0])
        dir_vec_y = float(dir_vec[1])
        dir_vec_z = float(dir_vec[2])
        point_x = float(point[0])
        point_y = float(point[1])
        point_z = float(point[2])
        s = (np.linspace(-5, 5, 100) - point_x)/dir_vec_x
        x = point_x + dir_vec_x*s
        y = point_y + dir_vec_y*s
        z = point_z + dir_vec_z*s
        ax.plot(x, y, z, color=color)
    if len(dir_vec) == 2:
        ax = plt.gca()
        ax.set_aspect("equal")
        dir_vec_x = float(dir_vec[0])
        dir_vec_y = float(dir_vec[1])
        point_x = float(point[0])
        point_y = float(point[1])
        s = (np.linspace(-5, 5, 100) - point_x)/dir_vec_x
        x = point_x + dir_vec_x*s
        y = point_y + dir_vec_y*s
        ax.plot(x, y, color=color)


def plot_plane(normal, d, color=None, xrange=[-5,5], yrange=[-5,5]):
    """
    Plots the plane whose general equation is normal . (x,y,z) = d.
    If normal is a 2-vector, plots a line (2D plot).
    """
    if len(normal) == 3:
        ax = plt.gca(projection='3d')
        ax.set_aspect("equal")
        normal_x = float(normal[0])
        normal_y = float(normal[1])
        normal_z = float(normal[2])
        d = float(d)
        x = np.linspace(xrange[0], xrange[1], 100)
        y = np.linspace(yrange[0], yrange[1], 100)
        X, Y = np.meshgrid(x,y)
        if color is None:
            color_picker = PlaneColorPicker()
            color = color_picker.get_color()
        Z = (d - normal_x*X - normal_y*Y)/normal_z
        ax.plot_surface(X, Y, Z, color=color, alpha=0.2)
    if len(normal) == 2:
        ax = plt.gca()
        ax.set_aspect("equal")
        normal_x = float(normal[0])
        normal_y = float(normal[1])
        d = float(d)
        x = np.linspace(xrange[0], xrange[1], 100)
        y = (d - normal_x*x)/normal_y
        ax.plot(x, y, color=color)


# IMPLEMENTATION DETAILS
################################################################################

class Arrow3D(FancyArrowPatch):
    """A 3D arrow used to represent vectors in 3D."""
    
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs
    
    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


class Arrow2D(FancyArrowPatch):
    """A 2D arrow used to represent vectors in 2D."""
    
    def __init__(self, xs, ys, *args, **kwargs):
        self._verts2d = xs, ys
        FancyArrowPatch.__init__(self, (xs[0],ys[0]), (xs[1],ys[1]), *args, **kwargs)
    
    def draw(self, renderer):
        xs3d, ys3d = self._verts2d
        xs, ys = xs3d, ys3d
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


# HELPER FUNCTIONS
################################################################################
 
def autoscale_arrows(ax=None):
    """
    Custom auto-scaling method for Arrow3D objects.
    """
    if ax is None:
        ax = plt.gca()
    arrow3Ds = [ ch for ch in ax.get_children() if type(ch) == Arrow3D ]
    arrow2Ds = [ ch for ch in ax.get_children() if type(ch) == Arrow2D ]
    if arrow2Ds and arrow3Ds:
        print('Mixing Arrow2D and Arrow3D not supported') 
        return -1
    if arrow3Ds:
        all_xs, all_ys, all_zs = [], [], []
        for arrow in arrow3Ds:
            all_xs.append(arrow._verts3d[0][0])
            all_xs.append(arrow._verts3d[0][1])
            all_ys.append(arrow._verts3d[1][0])
            all_ys.append(arrow._verts3d[1][1])
            all_zs.append(arrow._verts3d[2][0])
            all_zs.append(arrow._verts3d[2][1])
        min_x, max_x = min(all_xs), max(all_xs)
        min_y, max_y = min(all_ys), max(all_ys)
        min_z, max_z = min(all_zs), max(all_zs)
        cube_side = max(max_x-min_x, max_y-min_y, max_z-min_z)
        ax.set_xlim(min_x, min_x + cube_side)
        ax.set_ylim(min_y, min_y + cube_side)
        ax.set_zlim(min_z, min_z + cube_side)
    if arrow2Ds:
        all_xs, all_ys = [], []
        for arrow in arrow2Ds:
            all_xs.append(arrow._verts2d[0][0])
            all_xs.append(arrow._verts2d[0][1])
            all_ys.append(arrow._verts2d[1][0])
            all_ys.append(arrow._verts2d[1][1])
        min_x, max_x = min(all_xs), max(all_xs)
        min_y, max_y = min(all_ys), max(all_ys)
        square_side = max(max_x-min_x, max_y-min_y)
        ax.set_xlim(min_x, min_x + square_side)
        ax.set_ylim(min_y, min_y + square_side)


class PlaneColorPicker:
    """
    A singleton class that cycles through the colors used for drawing planes.
    """
    COLORS = ['b', 'g', 'r', 'c', 'm', 'k']
    instance = None
    class __PlaneColorPicker:
        def __init__(self, start_index):
            self.color_index = start_index
        def __get_color(self):
            cur = self.color_index
            self.color_index = (cur + 1) % len(PlaneColorPicker.COLORS)
            return PlaneColorPicker.COLORS[cur]
    def __init__(self, start=0):
        if not PlaneColorPicker.instance:
            PlaneColorPicker.instance = PlaneColorPicker.__PlaneColorPicker(start)
    def get_color(self):
        return self.instance.__get_color()
