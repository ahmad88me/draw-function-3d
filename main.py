'''
=================
3D wireframe plot
=================

A very basic demonstration of a wireframe plot.
'''


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox
import numpy as np
from functools import partial
from mathparser import MathParser


PARSER = 'eval'  # eval or text
math_parser = MathParser()
initial_formula = "(x*x) - (y*y)"

fig, ax, plot = None, None, None


def get_graph_data(f, x_min, x_max, y_min, y_max):
    x_step = (x_max-x_min)/50.0
    y_step = (y_max-y_min)/50.0
    X = np.arange(x_min, x_max, x_step)
    Y = np.arange(y_min, y_max, y_step)
    zlist = []
    xy_note = []
    for x in X:
        for y in Y:
            try:
                z = f(x=x, y=y)
                zlist.append(z)
            except Exception as e:
                print "exception: "+str(e)
                xy_note.append((x, y))
                z = 0
                zlist.append(0.0)
    Z = np.array(zlist)
    Z = Z.reshape(len(X), len(Y))
    X, Y = np.meshgrid(X, Y)
    print "Z: "
    print Z
    return X, Y, Z


def submit(text):
    global f, ax, plot
    f = partial(text_based_function, s=text)
    print "new formula: %s" % text
    X, Y, Z = get_graph_data(f, x_min=-50, x_max=50, y_min=-50, y_max=50)
    ax.clear()
    plot = ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')
    plt.draw()


def draw_init(X, Y, Z):
    global fig, ax, plot
    # Plot a basic wireframe.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    axbox = plt.axes([0.1, 0.05, 0.8, 0.075])
    text_box = TextBox(axbox, 'Evaluate', initial=initial_formula)
    text_box.on_submit(submit)

    plot = ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')
    plt.show()


def evaluate_math_expression(s):
    global math_parser
    try:
        return math_parser.evaluate(s)
    except Exception as e:
        print "error: "+str(e)
        return None


def ff(x, y):
    return x*x - y*y


def text_based_function(s, x, y):
    s.replace("x", str(x))
    subst = s.replace("x", str(x)).replace("y", str(y))
    if PARSER == 'eval':
        return eval(s)
    elif PARSER == 'text':
        return evaluate_math_expression(subst)
    else:
        print "Invalid PARSER"
        return None

f = partial(text_based_function, s=initial_formula)
draw_init(*get_graph_data(f, x_min=-50, x_max=50, y_min=-50, y_max=50))
