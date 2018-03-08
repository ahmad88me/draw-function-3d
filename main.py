'''
=================
3D wireframe plot
=================

A very basic demonstration of a wireframe plot.
'''


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox, Button
import numpy as np
from functools import partial
from mathparser import MathParser
from math import log, log10


# import numpy as np
# np.seterr(divide='ignore', invalid='ignore')

WIRE = True
PARSER = 'eval'  # eval or text
math_parser = MathParser()
# initial_formula = "(x*x) - (y*y)"
# initial_x_range = "-50, 50"
# initial_y_range = "-50, 50"

initial_formula = "(1-x) - (1.0/(log(y+1)+1))"
initial_x_range = "0, 1"
initial_y_range = "0,20"

fig, ax, plot = None, None, None


def get_graph_data(f, x_min, x_max, y_min, y_max):
    x_step = (x_max-x_min)/50.0
    y_step = (y_max-y_min)/50.0
    # x_step = (x_max-x_min)/200.0
    # y_step = (y_max-y_min)/200.0
    X = np.arange(x_min, x_max, x_step)
    Y = np.arange(y_min, y_max, y_step)
    zlist = []
    xy_note = []
    X2 = []
    Y2 = []
    Z2 = []
    for x in X:
        for y in Y:
            try:
                z = f(x=x, y=y)
                if z is None:
                    z = 100.0

            except Exception as e:
                print "exception: "+str(e)
                xy_note.append((x, y))
                z = 100.0

            zlist.append(z)
    Z = np.array(zlist)
    Z = Z.reshape(len(X), len(Y))
    X, Y = np.meshgrid(X, Y)
    print "Z: "
    print Z
    return X, Y, Z


def submit(text):
    global f, ax, plot, x_max, x_min, y_max, y_min, initial_formula, WIRE
    initial_formula = text
    f = partial(text_based_function, s=text)
    print "new formula: %s" % text
    X, Y, Z = get_graph_data(f, x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
    ax.clear()
    if WIRE:
        plot = ax.plot_wireframe(X, Y, Z, rcount=len(Y[0]) / 4, ccount=len(X[0]) / 4)
    else:
        plot = ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')

    plt.draw()


def toggle_wire(event):
    global WIRE, initial_formula
    WIRE = not WIRE
    submit(initial_formula)


def set_x_range(x_range_text):
    global x_max, x_min
    b, a = x_range_text.split(',')
    x_min = float(b)
    x_max = float(a)


def set_y_range(y_range_text):
    global y_max, y_min
    b, a = y_range_text.split(',')
    y_min = float(b)
    y_max = float(a)


def draw_init(X, Y, Z):
    global fig, ax, plot, text_box
    # Plot a basic wireframe.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    axbox = plt.axes([0.2, 0.06, 0.7, 0.075])
    text_box = TextBox(axbox, 'Evaluate', initial=initial_formula)
    text_box.on_submit(submit)

    xbox = plt.axes([0.2, 0, 0.3, 0.075])
    x_text_box = TextBox(xbox, 'X_range', initial=initial_x_range)
    x_text_box.on_submit(set_x_range)

    ybox = plt.axes([0.6, 0, 0.3, 0.075])
    y_text_box = TextBox(ybox, 'Y_range', initial=initial_y_range)
    y_text_box.on_submit(set_y_range)

    bbox = plt.axes([0, 0.9, 0.1, 0.1])
    b = Button(bbox, '(un)wire')
    b.on_clicked(toggle_wire)

    if WIRE:
        plot = ax.plot_wireframe(X, Y, Z, rcount=len(Y[0]) / 4, ccount=len(X[0]) / 4)
    else:
        plot = ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')

    plt.show()


def evaluate_math_expression(s):
    global math_parser
    try:
        return math_parser.evaluate(s)
    except ZeroDivisionError:
        print "division by zero"
        return None
    except Exception as e:
        print "error: "+str(e)
        return None


def text_based_function(s, x, y):
    s.replace("x", str(x))
    subst = s.replace("x", str(x)).replace("y", str(y))
    if PARSER == 'eval':
        try:
            return eval(s)
        except ZeroDivisionError:
            print "division by zero"
            return None
        except:
            return None
    elif PARSER == 'text':
        try:
            return evaluate_math_expression(subst)
        except:
            return None
    else:
        print "Invalid PARSER"
        return None

x_min = -50
y_min = -50
x_max = 50
y_max = 50
f = partial(text_based_function, s=initial_formula)
draw_init(*get_graph_data(f, x_min=-50, x_max=50, y_min=-50, y_max=50))
