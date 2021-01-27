import math
import global_vars as gv

def f_plus(x,y):
    try:
        f = x+y
    except:
        gv.err = "error in '+' function"
        return None
    return f


def f_minus(x,y):
    try:
        f = x-y
    except:
        gv.err = "error in '-' function"
        return None
    return f


def f_mul(x,y):
    try:
        f = x*y
    except:
        gv.err = "error in '*' function"
        return None
    return f


def f_abs(x, y=1):
    try:
        f = math.fabs(x)
    except:
        gv.err = "error in 'abs' function"
        return None
    return f


def f_div(x,y):
    try:
        f = x/y
    except ZeroDivisionError:
        gv.err = (f"illegal division by 0")
        return None
    except:
        gv.err = "error in '/' function"
        return None
    return f


def f_pow(x,y):
    try:
        f = math.pow(x,y)
    except ValueError:
        gv.err = (f"can't power   {x} ^ {y}")
        return None
    except:
        gv.err = "error in '^' function"
        return None
    return f


def f_frac(x, y=1.0):
    try:
        f = math.factorial(x)
    except ValueError:
        gv.err = (f"can't fractorial {x}")
        return None
    except:
        gv.err = "error in '!' function"
        return None
    return f


def f_sqrt(x, y=1.0):
    try:
        f = math.pow(x,0.5)
    except ValueError:
        gv.err = (f"can't sqrt negative ({x})")
        return None
    except:
        gv.err = "error in 'sqrt' function"
        return None
    return f


def f_ln(x, y=1.0):
    try:
        f = math.log(x,math.e)
    except ValueError:
       gv.err = (f"can't ln ({x})")
       return 0
    except:
        gv.err = "error in 'ln' function"
        return None
    return f


def f_log(x, y):
    try:
        f = math.log(y, x)
    except ValueError:
       gv.err = (f"can't log({x},{y})")
       return 0
    except:
        gv.err = "error in 'log' function"
        return None
    return f


def f_sin(x, y=1.0):
    try:
        if gv.degree == 'Rad':
            f = math.sin(x)
        else:
            f = math.sin(x*math.pi/180)
    except:
        gv.err = "error in 'sin' function"
        return None
    return f


def f_cos(x, y=1.0):
    try:
        if gv.degree == 'Rad':
            f = math.cos(x)
        else:
            f = math.cos(x*math.pi/180)
    except:
        gv.err = "error in 'cos' function"
        return None
    return f


def f_tan(x, y=1.0):
    try:
        if gv.degree == 'Rad':
            f = math.tan(x)
        else:
            f = math.tan(x*math.pi/180)
    except:
        gv.err = f"error in 'tan' function"
        return None
    return f


def f_pi(x=1.0, y=1.0):
    return math.pi


def f_e(x=1.0, y=1.0):
    return math.e


def f_x(x=1.0, y=1.0):
    return gv.x


def f_y(x=1.0, y=1.0):
    return gv.y


def f_num(x, y):
    gv.err = "unexpected 'number' function in m_function"
    return None
