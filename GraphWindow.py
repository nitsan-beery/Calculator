import tkinter as tk
import global_vars as gv
from global_vars import Point
import func_tree as ft
import math


def toggle(self, b):
    if b.config('relief')[-1] == 'sunken':
        b.config(relief="raised")
        return 'off'
    else:
        b.config(relief="sunken")
        return 'on'


widget_names = {
    'in': '''zoom in
mouse wheel or key ,''',
    'out': '''zoom out
mouse wheel or key .''',
    '1:1': '''reset proportions 1:1
key 5 or 1''',
    '0,0': '''reset to position 0,0
key 0''',
    chr(708): '''change proportion x/y
key a''',
    chr(709): '''change proportion x/y
key z'''
}


class GraphWindow:
    def __init__(self, master, exp, root, l, x_minus=-gv.DEFAULT_AXE_X, x_plus=gv.DEFAULT_AXE_X, min_y=-gv.DEFAULT_AXE_Y, max_y=gv.DEFAULT_AXE_Y):
        exp = ' y = '+exp
        self.window_main = tk.Tk(className=exp)
        gx = '+'+str(master.window_main.winfo_x()+master.window_main.winfo_width())
        gy = '+'+str(master.window_main.winfo_y())
        g = gx+gy
        self.window_main.geometry(g)

        self.frame_1 = tk.Frame(self.window_main)   
        self.frame_1.pack(fill='both', side='top', expand=1)
        self.frame_2 = tk.Frame(self.window_main, borderwidth=1, relief=tk.SUNKEN, bg='#C5ECFF')
        self.frame_2.pack(fill='both', side='bottom')

        self.board = tk.Canvas(self.frame_1, height=gv.GRAPH_WINDOW_HEIGHT, width=gv.GRAPH_WINDOW_WIDTH)
        self.board.pack(fill=tk.BOTH)

        self.label_help = tk.Label(self.frame_2, text="        move           zoom      proportion    position  "
                                                      "    x/y               resolution                        infinity", bg='#C5ECFF')
        self.label_help.grid(row=0, columnspan=20, pady=2, sticky='W')

        self.label_move = tk.Label(self.frame_2, text=' arrow keys ')
        self.label_move.grid(row=1, column=0, padx=5)
        self.button_zoom_in = tk.Button(self.frame_2, text='in', command=lambda: self.zoom_xy(10/12))
        self.button_zoom_in.grid(row=1, column=1, sticky='E')
        self.button_zoom_out = tk.Button(self.frame_2, text='out', command=lambda: self.zoom_xy(12/10))
        self.button_zoom_out.grid(row=1, column=2, sticky='W')
        self.button_1_1 = tk.Button(self.frame_2, text='1:1', command=lambda: self.set_1_to_1_xy_proportions())
        self.button_1_1.grid(row=1, column=3, sticky='E', padx=20)
        self.button_0_0 = tk.Button(self.frame_2, text='0,0', command=lambda: self.reset_00())
        self.button_0_0.grid(row=1, column=4, sticky='E', padx=20)
        self.button_x_to_y_up = tk.Button(self.frame_2, text=chr(708), command=lambda: self.zoom_y(10/12))
        self.button_x_to_y_up.grid(row=1, column=5, sticky='E')
        self.button_x_to_y_down = tk.Button(self.frame_2, text=chr(709), command=lambda: self.zoom_y(12/10))
        self.button_x_to_y_down.grid(row=1, column=6, sticky='W')
        self.label_empty21 = tk.Label(self.frame_2, text='', width=1, bg='#C5ECFF')
        self.label_empty21.grid(row=1, column=7)
        self.slider_resolution = tk.Scale(self.frame_2, orient=tk.HORIZONTAL, length=100, showvalue=0, from_=10, to=6000, resolution=10)
        self.slider_resolution.grid(row=1, column=8, sticky='W')
        self.slider_infi = tk.Scale(self.frame_2, orient=tk.HORIZONTAL, length=100, showvalue=0, from_=10, to=gv.INFINITY*3, resolution=10)
        self.slider_infi.grid(row=1, column=9, sticky='W', padx=10)
        self.button_f_tag = tk.Button(self.frame_2, text="f'", command=lambda: self.toggle_f_tag())
        self.button_f_tag.grid(row=1, column=10, sticky='E', padx=5)

        self.slider_resolution.set(gv.points_in_list)
        self.slider_infi.set(gv.INFINITY)

        self.window_main.update()

        self.master = master
        self.root = root
        self.f_list = l
        self.f_tag_list = None
        self.show_f_tag = False
        self.x_minus = float(x_minus)
        self.x_plus = float(x_plus)
        self.y_minus = float(min_y)
        self.y_plus = float(max_y)
        if self.y_plus == self.y_minus:
            self.y_minus -= 5
            self.y_plus += 5

        # number of pixels for increment x 1
        self.pixels_for_1_x = float((self.frame_1.winfo_width()-gv.UNKNOWN_BORDER)/(self.x_plus-self.x_minus))
        # number of pixels for increment y 1
        self.pixels_for_1_y = float((self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)/(self.y_plus-self.y_minus))
        # (0,0) position on screen
        self.zero = Point(-self.x_minus*self.pixels_for_1_x, self.y_plus*self.pixels_for_1_y)

        self.cursor_line_x = None
        self.cursor_line_y = None
        self.cursor_position = None
        self.cursor_text = None
        self.num_point_text = None
        self.infi_text = None

        self.board.bind('<Button-1>', self.mouse_1_pressed)
        self.board.bind('<B1-Motion>', self.mouse_1_motion)
        self.board.bind('<ButtonRelease-1>', self.mouse_button_released)
        self.board.bind('<Button-3>', self.mouse_3_pressed)
        self.board.bind('<B3-Motion>', self.mouse_3_motion)
        self.board.bind('<ButtonRelease-3>', self.mouse_button_released)
        self.board.bind('<MouseWheel>', self.mouse_wheel)
        self.window_main.bind('<Key>', self.key)
        self.window_main.bind('<Configure>', self.change_window_size)
        self.button_zoom_in.bind('<Button-1>', self.mouse_press_button)
        self.button_zoom_out.bind('<Button-1>', self.mouse_press_button)
        self.button_1_1.bind('<Button-1>', self.mouse_press_button)
        self.button_0_0.bind('<Button-1>', self.mouse_press_button)
        self.slider_resolution.bind('<Button-1>', self.change_resolution)
        self.slider_resolution.bind('<B1-Motion>', self.change_resolution)
        self.slider_resolution.bind('<ButtonRelease-1>', self.set_resolution)
        self.slider_infi.bind('<Button-1>', self.change_infi)
        self.slider_infi.bind('<B1-Motion>', self.change_infi)
        self.slider_infi.bind('<ButtonRelease-1>', self.set_infi)
        self.button_x_to_y_up.bind('<Button-1>', self.mouse_press_button)
        self.button_x_to_y_down.bind('<Button-1>', self.mouse_press_button)

    def mouse_wheel(self, event):
        if event.delta > 0:
            self.zoom_xy(1.2)
        else:
            self.zoom_xy(0.8)

    def change_window_size(self, event):
        self.frame_2.config(height=self.frame_2.winfo_height())
        self.board.config(height=self.window_main.winfo_height()-self.frame_2.winfo_height()-gv.UNKNOWN_BORDER,
                          width=self.window_main.winfo_width()-self.frame_2.winfo_width()-gv.UNKNOWN_BORDER)
        self.update_view()

    def change_resolution(self, event):
        if self.num_point_text is not None:
            self.board.delete(self.num_point_text)
        r = self.slider_resolution.get()
        t = f'number of points: {r}'
        self.num_point_text = self.board.create_text(0+gv.UNKNOWN_BORDER, 0+gv.UNKNOWN_BORDER, text=t, anchor='nw', fill=gv.short_cut_text_color)

    def set_resolution(self, event):
        if self.num_point_text is not None:
            self.board.delete(self.num_point_text)
        r = self.slider_resolution.get()
        gv.points_in_list = r
        self.update_view(True)

    def change_infi(self, event):
        if self.infi_text is not None:
            self.board.delete(self.infi_text)
        i = self.slider_infi.get()
        t = f'infinity limit: {i}'
        self.infi_text = self.board.create_text(0+gv.UNKNOWN_BORDER, 0+gv.UNKNOWN_BORDER, text=t, anchor='nw', fill=gv.short_cut_text_color)

    def set_infi(self, event):
        if self.infi_text is not None:
            self.board.delete(self.infi_text)
        i = self.slider_infi.get()
        gv.INFINITY = i
        self.update_view(True)

    def zoom_y(self, z):
        self.y_plus *= z
        self.y_minus *= z
        self.update_view()

    def zoom_xy(self, z):
        span = self.x_plus-self.x_minus
        mid_x = self.x_minus + span/2
        span *= z
        self.x_plus = mid_x + span/2
        self.x_minus = mid_x - span/2
        self.y_plus *= z
        self.y_minus *= z
        self.update_view(True)

    def set_1_to_1_xy_proportions(self):
        screen_ratio = math.fabs((self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)/(self.frame_1.winfo_width()-gv.UNKNOWN_BORDER))
        xy_ratio = float((self.y_plus - self.y_minus)/(self.x_plus - self.x_minus))
        self.y_plus = self.y_plus/xy_ratio*screen_ratio
        self.y_minus = self.y_minus/xy_ratio*screen_ratio
        self.update_view()

    def reset_00(self):
        spanx = self.x_plus-self.x_minus
        spany = self.y_plus-self.y_minus
        self.x_minus = -spanx/2
        self.x_plus = spanx/2
        self.y_minus = -spany/2
        self.y_plus = spany/2
        self.update_view(True)

    def move_x(self, d):
        span = self.x_plus-self.x_minus
        self.x_minus = self.x_minus+span*d
        self.x_plus = self.x_plus+span*d
        self.update_view(True)

    def move_y(self, d):
        span = self.y_plus-self.y_minus
        self.y_minus = self.y_minus+span*d
        self.y_plus = self.y_plus+span*d

        self.update_view(True)

    def update_view(self, recalculate_list=False):
        tmp_px = self.pixels_for_1_x
        tmp_py = self.pixels_for_1_y
        try:
            self.pixels_for_1_x = float((self.frame_1.winfo_width()-gv.UNKNOWN_BORDER)/(self.x_plus-self.x_minus))
        except:
            self.pixels_for_1_x = tmp_px
        try:
            self.pixels_for_1_y = float((self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)/(self.y_plus-self.y_minus))
        except:
            self.pixels_for_1_y = tmp_py
        self.zero = Point(-self.x_minus*self.pixels_for_1_x, self.y_plus*self.pixels_for_1_y)
        if recalculate_list:
            self.f_list = ft.get_result_list(self.root, self.x_minus, self.x_plus)
            if self.show_f_tag:
                self.get_f_tag_list()
        self.board.delete('all')
        self.draw_axes()
        self.draw_f()
        if self.show_f_tag:
            self.draw_f_tag()

    def get_axe_x(self):
        left = 0, self.zero.y
        right = (self.frame_1.winfo_width()-gv.UNKNOWN_BORDER), self.zero.y
        return left, right

    def get_axe_y(self):
        top = self.zero.x, 0
        bottom = self.zero.x, (self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)
        return top, bottom

    def draw_axes(self):
        axe_x_left, axe_x_right = self.get_axe_x()
        axe_y_top, axe_y_bottom = self.get_axe_y()

        left_str = str(round(self.x_minus, 2))
        left_pos = axe_x_left
        right_str = str(round(self.x_plus, 2))
        right_pos = axe_x_right
        top_str = str(round(self.y_plus, 2))
        top_pos = axe_y_top
        bottom_str = str(round(self.y_minus, 2))
        bottom_pos = axe_y_bottom

        left_align = 'nw'
        right_align = 'ne'
        top_align = 'nw'
        bottom_align = 'sw'

        self.board.create_line(axe_x_left, axe_x_right)
        self.board.create_line(axe_y_top, axe_y_bottom)

        # no x axe in view
        if self.zero.y < 5:
            left_pos = 0, 0
            right_pos = (self.frame_1.winfo_width()-gv.UNKNOWN_BORDER), 0
        if self.zero.y > (self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)-5:
            left_pos = 0, (self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)
            right_pos = (self.frame_1.winfo_width()-gv.UNKNOWN_BORDER), (self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)
            left_align = 'sw'
            right_align = 'se'

        # no y axe in view
        if self.zero.x < 5:
            top_pos = (self.frame_1.winfo_width()-gv.UNKNOWN_BORDER), 0
            bottom_pos = (self.frame_1.winfo_width()-gv.UNKNOWN_BORDER), (self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)
            top_align = 'ne'
            bottom_align = 'se'
        if self.zero.x > (self.frame_1.winfo_width()-gv.UNKNOWN_BORDER)-5:
            top_pos = 0, 0
            bottom_pos = 0, (self.frame_1.winfo_height()-gv.UNKNOWN_BORDER)

        self.board.create_text(left_pos, text=left_str, anchor=left_align)
        self.board.create_text(right_pos, text=right_str, anchor=right_align)
        self.board.create_text(top_pos, text=top_str, anchor=top_align)
        self.board.create_text(bottom_pos, text=bottom_str, anchor=bottom_align)

    def draw_graph(self, l, c):
        for line in l:
            prev_point = None
            for point in line:
                if prev_point is not None:
                    self.draw_line(prev_point, point, c)
                prev_point = point
                
    def draw_f(self):
        self.draw_graph(self.f_list, gv.f_color)

    def draw_f_tag(self):
        if self.f_tag_list is not None:
            self.draw_graph(self.f_tag_list, gv.f_tag_color)

    def toggle_f_tag(self):
        if toggle(self, self.button_f_tag) == 'on':
            self.get_f_tag_list()
            self.show_f_tag = True
        else:
            self.show_f_tag = False
        self.update_view()

    def get_f_tag_list(self):
        if self.f_list is None:
            return None
        self.f_tag_list = []
        tmp_l = []
        for line in self.f_list:
            prev_point = None
            for point in line:
                if prev_point is not None:
                    p = Point()
                    p.x = (point.x+prev_point.x)/2
                    p.y = float((point.y-prev_point.y)/(point.x-prev_point.x))
                    tmp_l.append(p)
                prev_point = point
            self.f_tag_list.append(tmp_l)
            tmp_l = []
            
    # convert (x,y) to positions on screen and draw line between p1 and p2
    def draw_line(self, p1, p2, c):
        p1 = self.convert_xy_to_screen(p1)
        p2 = self.convert_xy_to_screen(p2)
        self.board.create_line(p1.x, p1.y, p2.x, p2.y, fill=c)

    def convert_xy_to_screen(self, p):
        cp = Point()
        cp.x = float(self.zero.x + p.x * self.pixels_for_1_x)
        cp.y = float(self.zero.y - p.y * self.pixels_for_1_y)
        return cp

    def convert_screen_to_xy(self, p):
        cp = Point()
        cp.x = float(p.x - self.zero.x)/self.pixels_for_1_x
        cp.y = float(self.zero.x - p.y)/self.pixels_for_1_y
        return cp

    def get_nearest_point_from_list(self, x, l):
        for list in l:
            for point in list:
                if point.x >= x:
                    if point.x-x <= (self.x_plus - self.x_minus)/gv.points_in_list:
                        return point
        return None

    def mouse_button_pressed(self, event, l):
        p = Point(event.x, event.y)
        p = self.convert_screen_to_xy(p)
        x = p.x
        p = self.get_nearest_point_from_list(p.x, l)
        if p is None:
            t = f'({round(x, 2)}    E)'
            p = Point(x, 0)
        else:
            t = f'({round(p.x, 2)}    {round(p.y, 2)})'
        p = self.convert_xy_to_screen(p)
        self.cursor_line_x = self.board.create_line(0, p.y, self.board.winfo_width(), p.y, fill=gv.cursor_color)
        self.cursor_line_y = self.board.create_line(event.x, 0, event.x, self.board.winfo_height(), fill=gv.cursor_color)
        self.cursor_text = self.board.create_text(event.x, event.y, text=t)


    def mouse_3_pressed(self, event):
        if not self.show_f_tag:
            return
        self.mouse_button_pressed(event, self.f_tag_list)

    def mouse_3_motion(self, event):
        self.mouse_button_released(event)
        self.mouse_3_pressed(event)

    def mouse_1_pressed(self, event):
        self.mouse_button_pressed(event, self.f_list)

    def mouse_1_motion(self, event):
        self.mouse_button_released(event)
        self.mouse_1_pressed(event)

    def mouse_button_released(self, event):
        self.board.delete(self.cursor_line_x)
        self.board.delete(self.cursor_line_y)
        self.board.delete(self.cursor_text)

    def mouse_press_button(self, event):
        button_text = event.widget.cget('text')
        t = widget_names.get(button_text)
        if button_text == '+' or button_text == '-':
            t += f'\nnumber of points: {gv.points_in_list}'
        self.board.create_text(0+gv.UNKNOWN_BORDER, 0+gv.UNKNOWN_BORDER, text=t, anchor='nw', fill=gv.short_cut_text_color)

    def key(self, event):
        if event.keycode == 90:     # z key
            self.zoom_y(1.2)
        elif event.keycode == 65:   # a key
            self.zoom_y(0.8)
        elif event.keycode == 37:   # <- key
            self.move_x(-0.1)
        elif event.keycode == 39:   # -> key
            self.move_x(0.1)
        elif event.keycode == 38:   # arrow up key
            self.move_y(0.1)
        elif event.keycode == 40:   # arrow down key
            self.move_y(-0.1)
        elif event.keycode == 188:   # , key
            self.zoom_xy(0.8)
        elif event.keycode == 190:   # . key
            self.zoom_xy(1.2)
        elif event.keycode == 101 or event.keycode == 53 or event.keycode == 49 or event.keycode == 97:   # 5 or 1 key
            self.set_1_to_1_xy_proportions()
        elif event.keycode == 96 or event.keycode == 48:  # 0 key
            self.reset_00()
