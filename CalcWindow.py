from GraphWindow import *
from func_tree import *
from Graph3D import *


class CalcWindow:

    def __init__(self):
        self.window_main = tk.Tk(className=' Calculator')
        self.window_main.geometry('350x245')
        self.window_main.resizable(0, 0)

        self.frame_1 = tk.Frame(self.window_main)
        self.frame_1.pack(side=tk.TOP, fill=tk.BOTH)
        self.frame_2 = tk.Frame(self.window_main)
        self.frame_2.pack(side=tk.TOP, fill=tk.BOTH, ipady=6)
        self.frame_3 = tk.Frame(self.window_main)
        self.frame_3.pack(side=tk.TOP, fill=tk.BOTH, ipady=0)
        self.frame_4 = tk.Frame(self.window_main)
        self.frame_4.pack(side=tk.TOP, fill=tk.BOTH, ipady=6)

        self.button_Deg = tk.Button(self.frame_1, text=gv.degree, width=3, relief='sunken', bg='#CCFFCC', command=lambda: self.switch_deg_rad())
        self.label_empty_11 = tk.Label(self.frame_1, text='')
        self.label_x = tk.Label(self.frame_1, text='x', padx=5)
        self.entry_x = tk.Entry(self.frame_1, width=4)
        self.label_y = tk.Label(self.frame_1, text='y', padx=5)
        self.entry_y = tk.Entry(self.frame_1, width=4)
        self.label_empty_12 = tk.Label(self.frame_1, text='')
        self.button_help = tk.Button(self.frame_1, text='Help', command=lambda: self.show_help())

        self.button_Deg.grid(row=0, column=0, sticky='W', ipadx=1, padx=5, pady=5)
        self.label_empty_11.grid(row=0, column=1, padx=38)
        self.label_x.grid(row=0, column=2)
        self.entry_x.grid(row=0, column=3)
        self.label_y.grid(row=0, column=4)
        self.entry_y.grid(row=0, column=5)
        self.label_empty_12.grid(row=0, column=6, padx=35)
        self.button_help.grid(row=0, column=7, sticky='E', padx=5, pady=5)

        self.entry_answer = tk.Entry(self.frame_2, text='', width=55, bg='#FFFFCC')
        self.entry_answer.grid(row=0, column=0, padx=5, pady=2)

        self.button_dim = tk.Button(self.frame_3, text='3D', width=4, bg='#B3FFFF', command=lambda: self.switch_dim())
        self.entry_axe_x_minus = tk.Entry(self.frame_3, width=5)
        self.entry_axe_x_plus = tk.Entry(self.frame_3, width=5)
        self.entry_axe_y_minus = tk.Entry(self.frame_3, width=5)
        self.entry_axe_y_plus = tk.Entry(self.frame_3, width=5)
        self.label_empty_31 = tk.Label(self.frame_3, text='')
        self.label_empty_32 = tk.Label(self.frame_3, text='')

        self.entry_axe_y_plus.grid(row=0, column=2)
        self.label_empty_31.grid(row=1, column=0, padx=45)
        self.label_empty_32.grid(row=2, column=0, columnspan=10, padx=150)
        self.button_dim.grid(row=1, column=2, pady=10)
        self.entry_axe_x_minus.grid(row=1, column=1, padx=5, sticky='E')
        self.entry_axe_x_plus.grid(row=1, column=3, padx=5, sticky='W')
        self.entry_axe_y_minus.grid(row=2, column=2)

        self.button_graph = tk.Button(self.frame_4, text='Graph', bg='#B3FFFF', command=lambda: self.show_graph())
        self.label_y_or_z = tk.Label(self.frame_4, text='z =', width=3)
        self.spinbox_func = tk.Spinbox(self.frame_4, width=48, values=gv.default_funcs)
        self.button_calculate = tk.Button(self.frame_4, text='Calculate', command=lambda: self.get_result())
        self.button_clear_exp = tk.Button(self.frame_4, text='Clear', command=lambda: self.reset_exp())

        self.label_y_or_z.grid(row=0, column=0, padx=5, pady=15, sticky='W')
        self.spinbox_func.grid(row=0, column=1, columnspan=3, sticky='W')
        self.button_graph.grid(row=1, column=0, columnspan=2, padx=5, sticky='W')
        self.button_calculate.grid(row=1, column=2, padx=20, columnspan=2, sticky='W')
        self.button_clear_exp.grid(row=1, column=3, sticky='E')

        self.entry_x.insert(0, gv.x)
        self.entry_y.insert(0, gv.y)
        self.entry_axe_x_minus.insert(0, -gv.DEFAULT_AXE_X)
        self.entry_axe_x_plus.insert(0, gv.DEFAULT_AXE_X)
        self.entry_axe_y_minus.insert(0, -gv.DEFAULT_AXE_Y)
        self.entry_axe_y_plus.insert(0, gv.DEFAULT_AXE_Y)

        if gv.is_2D:
            self.button_dim['text'] = '2D'
            self.label_y_or_z.config(text='y =')
            self.switch_dim()

        self.spinbox_func.focus_set()

        self.graph_window = None
        self.window_main.bind('<Key>', self.key)

    def show_graph(self):
        exp = self.spinbox_func.get()
        gv.is_2D = self.button_dim['text'] == '2D'

        try:
            x_minus = float(self.entry_axe_x_minus.get())
            x_plus = float(self.entry_axe_x_plus.get())
        except:
            self.entry_answer.delete(0, tk.END)
            self.entry_answer.insert(0, 'axe x invalid value')
            gv.err = None
            return

        if x_minus >= x_plus:
            self.entry_answer.delete(0, tk.END)
            self.entry_answer.insert(0, 'Illegal x range')
            gv.err = None
            return

        try:
            y_minus = float(self.entry_axe_y_minus.get())
            y_plus = float(self.entry_axe_y_plus.get())
        except:
            if gv.is_2D:
                y_plus = gv.DEFAULT_AXE_Y
                y_minus = -gv.DEFAULT_AXE_Y
            else:
                self.entry_answer.delete(0, tk.END)
                self.entry_answer.insert(0, 'axe y invalid value')
                gv.err = None
                return

        if y_minus >= y_plus:
            self.entry_answer.delete(0, tk.END)
            self.entry_answer.insert(0, 'Illegal y range')
            gv.err = None
            return

        is_default_y = (y_minus == -gv.DEFAULT_AXE_Y and y_plus == gv.DEFAULT_AXE_Y)

        root = get_tree_from_exp(exp)
        if gv.err != None:
            self.entry_answer.delete(0, tk.END)
            self.entry_answer.insert(0, gv.err)
            gv.err = None
            return

        if gv.is_2D:
            gv.points_in_list = gv.DEFAULT_POINTS_IN_2D_GRAPH
            l = get_result_list(root, x_minus, x_plus)
            self.graph_window = GraphWindow(self, exp, root, l, x_minus, x_plus, y_minus, y_plus)
            if is_default_y:
                self.graph_window.set_1_to_1_xy_proportions()
            self.graph_window.window_main.title = exp
            self.graph_window.update_view()
            self.graph_window.window_main.mainloop()
        else:
            gv.points_in_list = gv.DEFAULT_POINTS_IN_3D_GRAPH
            v_matrix, list_x, list_y = get_3D_matrix(root, x_minus, x_plus, y_minus, y_plus)
            node = get_f_plane_node(v_matrix, list_x, list_y)
            app = MyApp(node, exp, root, x_minus, x_plus, y_minus, y_plus)
            app.run()

    def switch_deg_rad(self):
        deg = self.button_Deg['text']
        if deg == 'Deg':
            gv.degree = 'Rad'
        else:
            gv.degree = 'Deg'

        self.button_Deg.config(text=gv.degree)

    def switch_dim(self):
        if toggle(self, self.button_dim) == 'on':
            gv.is_2D = True
            dimension = '2D'
            self.label_y_or_z.config(text='y =')
            self.entry_axe_y_minus.delete(0, tk.END)
            self.entry_axe_y_plus.delete(0, tk.END)
        else:
            gv.is_2D = False
            dimension = '3D'
            self.label_y_or_z.config(text='z =')
            if self.entry_axe_y_minus.get() == '':
                self.entry_axe_y_minus.insert(0, -gv.DEFAULT_AXE_Y)
                self.entry_axe_y_plus.insert(0, gv.DEFAULT_AXE_Y)

        self.button_dim.config(text=dimension)

    def show_help(self):
        self.entry_answer.delete(0, tk.END)
        h = 'use: '
        for item in VALID_USER_INPUT:
            h += f"{item}  "
        self.entry_answer.insert(0, h)

    def reset_exp(self):
        self.spinbox_func.delete(0, tk.END)
        self.entry_answer.delete(0, tk.END)

    def get_result(self):
        self.entry_answer.delete(0, tk.END)
        exp = self.spinbox_func.get()
        gv.x = float(self.entry_x.get())
        gv.y = float(self.entry_y.get())
        r = get_result_from_expression(exp)
        if gv.err == None:
            self.entry_answer.insert(0, r)
        else:
            self.entry_answer.insert(0, gv.err)
            gv.err = None

    def key(self, event):
        if event.keycode == 13:
            self.get_result()
