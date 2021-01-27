err = None
is_test_mode = False
is_debug_mode = False

x = y = 1.0

GRAPH_WINDOW_HEIGHT = 400
GRAPH_WINDOW_WIDTH = 500
UNKNOWN_BORDER = 4

DEFAULT_POINTS_IN_2D_GRAPH = GRAPH_WINDOW_WIDTH
DEFAULT_POINTS_IN_3D_GRAPH = 102

points_in_list = DEFAULT_POINTS_IN_3D_GRAPH
DEFAULT_AXE_X = 5
DEFAULT_AXE_Y = 5
DEFAULT_3D_AXE = DEFAULT_AXE_X

INFINITY = DEFAULT_AXE_Y*3
ROUND_DIGITS = 9
MIN_VERTICES_IN_VALID_LIST = 0

is_2D = True

degree = 'Rad'

f_color = 'blue'
f_tag_color = 'red'
cursor_color = 'green'
short_cut_text_color = 'green'

# 3D window
background_color = (51/255, 153/255, 1)
line_color = 1, 1, 0    # RGB 0-1
axe_color = 1, 0, 0
z_axe_color = (255/255, 153/255, 51/255)

default_funcs = ('',
                 '3(sin(9-x^2-y^2)/(9-x^2-y^2))^2+2(sin(x)/x*sin(y)/y)^6',
                 'ln(x)*ln(y)',
                 'sin(x)^2+cos(y)^2-sin(y)^2-cos(x)^2',
                 '3(sin(x)/x*sin(y)/y)',
                 'ln(abs(sin(x*y/3)))+2',
                 '((x/2.5)^2*y^3-((x/2.5)^2+y^2-1)^3)+3-5(sin(x)/x*sin(y)/y)^4',
                 '(x+y)/(1.5sqrt(x*y))',
                 'log(abs(x), y)/2',
                 'ln(sqrt(x^4+y^4))',
                 '-25/(x^2+y^2)+3',
                 'sqrt(x^4+y^4)/4-5',
                 '1/(x*y)',
                 'ln(abs(x*y))',
                 '3(sin(x)/x*sin(y)/y)^4',
                 '3(sin(9-x^2-y^2)/(9-x^2-y^2))^2',
                 '')


widget_text_scale = 0.05
widget_header_row = -0.85
widget_help_row = 1
widget_help_col = -1.4
widget_col_left = -1.15
widget_row_right_pos = 1.15
widget_row_height = 0.06
widget_col_size = 0.3
widget_header_color = 0, 1, 0, 1
widget_value_color = 0, 1, 0, 1

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


class Point3D:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z








