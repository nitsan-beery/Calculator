from global_vars import Point3D
from m_funcs import *
from parse import *
from GraphWindow import Point
from create_lines import *

NUM_PRIORITY = 7
PARENTHESIS_PRIORITY = 9

# function, priority
func_switcher = {
    '+': (f_plus, 0),
    '-': (f_minus, 0),
    '*': (f_mul, 1),
    '/': (f_div, 1),
    '^': (f_pow, 2),
    'sqrt': (f_sqrt, 3),
    'abs': (f_abs, 3),
    'ln': (f_ln, 3),
    'log': (f_log, 3),
    'sin': (f_sin, 3),
    'cos': (f_cos, 3),
    'tan': (f_tan, 3),
    '!': (f_frac, 4),
    'pi': (f_pi, NUM_PRIORITY),
    'e': (f_e, NUM_PRIORITY),
    'x': (f_x, NUM_PRIORITY),
    'y': (f_y, NUM_PRIORITY),
    'number': (f_num, NUM_PRIORITY)
}


def set_func_priority(f):
    if len(f) > 1 and f[0] == '-':
        f = f[1:]
    return func_switcher.get(f)[1]


def m_function(f, x=1.0, y=1.0):
    sign = 1

    if (is_func(f) or is_special_num(f)) and len(f) > 1 and f[0] == '-':
        f = f[1:]
        sign = -1

    result = func_switcher.get(f)[0](x, y)
    if gv.err is None:
        return sign * result
    else:
        return None


def is_valid_data_for_tree(f):
    return is_num(f) or is_func(f) is not None


def get_result_from_node(n):
    answer = None

    if gv.err is not None:
        return 1

    elif n.func.f == 'number':
        answer = n.data

    elif is_middle_operator(n.func.f) or is_func_x_y(n.func.f):
        if n.left is None or n.right is None:
            gv.err = "Function '" + n.func.f + "' expecting 2 values"
        else:
            answer = m_function(n.func.f, get_result_from_node(n.left), get_result_from_node(n.right))

    elif is_func_x(n.func.f) or is_right_operator(n.func.f):
        if n.right is None:
            gv.err = "Function '" + n.func.f + "'missing value"
            return None
        else:
            answer = m_function(n.func.f, get_result_from_node(n.right))

    elif is_special_num(n.func.f):
        answer = m_function(n.func.f)

    if gv.err is not None:
        return 1
    else:
        return answer


class Func:
    def __init__(self):
        self.f = None
        self.priority = 0


class FunctionNode:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None
        self.func = Func()

    def get_result_from_node(self):
        return get_result_from_node((self))

    def set_priority(self, p):
        self.func.priority = p

    def insert_data(self, f):
        if is_valid_data_for_tree(f):
            if is_num(f):
                self.data = float(f)
                self.func.f = 'number'
                self.func.priority = NUM_PRIORITY
            else:
                self.func.f = f
                self.func.priority = set_func_priority(f)
        else:
            gv.err = ("Invalid data: '" + f + "'")


def insert_node(root, n):
    answer = root

    # empty tree
    if root is None or root.func.f is None:
        answer = n

    elif not is_valid_data_for_tree(n.func.f):
        gv.err = "unknown function '" + n.func.f + "'"

    elif is_right_operator(n.func.f) and n.func.priority != PARENTHESIS_PRIORITY:
        if n.func.priority > root.func.priority:
            root.right = insert_node(root.right, n)

        else:
            n.right = root
            answer = n

    # insert according to priority
    else:
        if n.func.priority > root.func.priority:
            root.right = insert_node(root.right, n)
        else:
            n.left = root
            answer = n

    return answer


def build_tree(root, list):
    position = 0
    for item in list:
        n = FunctionNode()

        # insert (expression) to the tree and remove it from list
        if item == '(':
            end = find_match_parenthesis(list[position:]) + position
            temp_list = list[position + 1:end]
            n = build_tree(n, temp_list)
            n.set_priority(PARENTHESIS_PRIORITY)
            del list[position:end]

        # insert simple expression (no parenthesis)
        else:
            n.insert_data(item)

        if gv.err is not None:
            return None

        root = insert_node(root, n)
        if gv.err is not None:
            return None

        position += 1

    return root


def get_lines_from_vertex_matrix(vertex_matrix, info):
    if vertex_matrix is None:
        print('DEBUG: in get_lines_from_vertex_matrix - empty vertex matrix')
        return None

    l_x = []
    l_y = []
    num_rows = len(vertex_matrix)
    num_cols = len(vertex_matrix[0])

    # check rows consistancy
    row = 0
    while row < num_rows:
        if len(vertex_matrix[row]) != num_cols:
            print(f'DEBUG: in get_lines_from_vertex_matrix inconsistant row {row}')
            vertex_matrix.pop(row)
            num_rows -= 1
        row += 1

    # adjust INFINITY in y lines
    for col in range(num_cols):
        prev_z = vertex_matrix[0][col].z
        for row in range(num_rows):
            z = vertex_matrix[row][col].z
            if z*prev_z < 0 and math.fabs(z-prev_z) > 2*gv.INFINITY:
                info[row][col] = False
            prev_z = z

    # arrange x_list
    for row in range(num_rows):
        tmp_l = []
        for col in range(num_cols):
            if info[row][col]:
                p = row*num_cols + col
                tmp_l.append(p)
            elif tmp_l != []:
                l_x.append(tmp_l)
                tmp_l = []
        if tmp_l != []:
            l_x.append(tmp_l)

    # arrange y_list
    for col in range(num_cols):
        tmp_l = []
        for row in range(num_rows):
            if info[row][col]:
                p = row*num_cols + col
                tmp_l.append(p)
            elif tmp_l != []:
                l_y.append(tmp_l)
                tmp_l = []
        if tmp_l != []:
            l_y.append(tmp_l)

    return l_x, l_y


def get_point3D_x_list(l, y):
    p = Point()
    update_list = []
    for point in range(len(l)):
        if l[point] is None:
            p3 = Point3D(p.x, y, p.y)
        else:
            p3 = Point3D(l[point].x, y, l[point].y)
        update_list.append(p3)
    return update_list

    
# return final_list_x of lines with constant y and variable x
# and final_list_y of lines out of vertices corresponding to final_list_x
def get_3D_matrix(root, min_x, max_x, min_y, max_y):
    vertex_matrix = []
    # holds information about number of lists in each line (min_x < x < max_x) and length of each list
    x_info = []
    step = float((max_y-min_y)/gv.points_in_list)

    y = min_y
    while y <= max_y:
        gv.y = y
        # get set of lists in range min_x - max_x each list ends only if there is division by x=0
        # if there is no division by 0 in the range min_x - max_x there will be only one list
        x_list, info = get_result_list(root, min_x, max_x)
        x_info.append(info)
        x_list = get_point3D_x_list(x_list, y)
        vertex_matrix.append(x_list)

        y = round(y + step, gv.ROUND_DIGITS)

    final_list_x, final_list_y = get_lines_from_vertex_matrix(vertex_matrix, x_info)

    return vertex_matrix, final_list_x, final_list_y


# return list of result for points in range min_x - max_x, None if can't get result for that x
# and info about index of None points in the list (True for valid, False for invalid)
def get_result_list(root, min_x, max_x):
    l = []
    info = []
    x = min_x
    prev_y = None

    step = float((max_x-min_x)/gv.points_in_list)

    while x <= max_x:
        is_valid_point = True
        gv.x = x
        y = round(get_result_from_node(root), gv.ROUND_DIGITS)
        if gv.err is not None:
            gv.err = None
            l.append(None)
            info.append(False)
            prev_y = None
            is_valid_point = False
        elif prev_y is not None:
            if y*prev_y < 0 and math.fabs(y-prev_y) > 2*gv.INFINITY:
                l.append(None)
                info.append(False)
                prev_y = y
                is_valid_point = False
        if is_valid_point:
            p = Point(x, y)
            prev_y = y
            l.append(p)
            info.append(True)
        x = round(x+step, gv.ROUND_DIGITS)
    if gv.is_2D:
        l = get_clean_list(l)
        return l

    else:
        return l, info


# return list of valid lines (no None point)
def get_clean_list(l):
    clean_list = []
    tmp_l = []
    for item in l:
        if item is not None:
            tmp_l.append(item)
            continue
        elif len(tmp_l) > gv.MIN_VERTICES_IN_VALID_LIST:
            clean_list.append(tmp_l)
        tmp_l = []

    if len(tmp_l) > gv.MIN_VERTICES_IN_VALID_LIST:
        clean_list.append(tmp_l)

    return clean_list


def get_tree_from_exp(exp):
    root = FunctionNode()

    l = parse(exp)
    if gv.err is not None:
        return None

    if gv.is_debug_mode:
        print(f'after parsing: {l}')

    root = build_tree(root, l)
    if gv.err is not None:
        return None

    return root


def get_result_from_expression(exp):
    root = get_tree_from_exp(exp)
    if gv.err is not None:
        return None
    else:
        f = root.get_result_from_node()
    if gv.err is not None:
        return None
    else:
        return f

