'''
=================
3D wireframe plot
=================

A very basic demonstration of a wireframe plot.
'''


from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
from functools import partial


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


def draw_init(X, Y, Z):
    # Plot a basic wireframe.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_surface(X, Y, Z, rcount=len(Y[0])/4, ccount=len(X[0])/4, cmap='plasma', edgecolor='none')
    plt.show()


def evaluate_math_expression(s):
    from fourFn import BNF, evaluateStack
    try:
        exprStack = BNF().parseString(s, parseAll=True)
        val = evaluateStack(exprStack[:])
        return val
    except Exception as e:
        print "error: "+str(e)
        return None


def ff(x, y):
    return x*x - y*y


def text_based_function(s, x, y):
    s.replace("x", str(x))
    subst = s.replace("x", str(x)).replace("y", str(y))
    return evaluate_math_expression(subst)



# f = partial(text_based_function, s="(x*x) - (y*y)")
# draw_init(*get_graph_data(f, x_min=-50, x_max=50, y_min=-50, y_max=50))

# print evaluate_math_expression(s="3*3 - 2*2")
# print type(evaluate_math_expression(s="3*3 - 2*2"))


# print text_based_function(s="x*x - y*y", x=1, y=2)


#draw_init(*get_graph_data(ff, x_min=-50, x_max=50, y_min=-50, y_max=50))
# draw(f=f, x_min=-50, x_max=50, y_min=-50, y_max=50)


s = "(3*2)-(2*1)"

# from fourFn import BNF, evaluateStack
# # print evaluate_math_expression(s)
# exprStack = BNF().parseString(s, parseAll=True)
# print exprStack
# val = evaluateStack(exprStack[:])
# print val

# from mathparser import MathParser
# mp = MathParser()
# print mp.evaluate(s)