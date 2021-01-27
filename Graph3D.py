from direct.showbase.MessengerGlobal import messenger
from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import WindowProperties
from panda3d.core import TextNode
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from convert_values import *
import global_vars as gv
from global_vars import Point3D
from func_tree import get_3D_matrix
from create_lines import get_f_plane_node



# create task that enables mouse-repeat event
class Repeater(DirectObject):
    """
    Repeat mouse button events while a button is held down.
    """

    def __init__(self, name, time):
        """
        Given a name of the event, e.g. mouse1, start
        sending name-repeat events every "time" seconds
        once event "name" is received until name-up is
        received.
        """
        self.time = time
        self.name = name
        self.task = None

        self.accept(name, self.start)
        self.accept(name + '-up', self.stop)

    def get_event(self):
        """
        Return the string that represents the event.
        """
        return '%s-repeat' % self.name

    def start(self):
        """
        Start sending repeat events.
        """
        if not self.task:
            self.task = taskMgr.doMethodLater(self.time, self.repeat,
                                              self.get_event())

    def stop(self):
        """
        Stop sending repeat events.
        """
        if self.task:
            taskMgr.remove(self.task)
            self.task = None

    def repeat(self, task):
        """
        Send repeat event.
        """
        messenger.send(self.get_event())
        return task.again


class MyApp(ShowBase):
    def __init__(self, f_plane_node=None, exp='z =', root=None,
                 x_minus=-gv.DEFAULT_3D_AXE, x_plus=gv.DEFAULT_3D_AXE, y_minus=-gv.DEFAULT_3D_AXE, y_plus=gv.DEFAULT_3D_AXE):
        ShowBase.__init__(self)

        # set window title
        props = WindowProperties()
        props.setTitle('z = '+exp)
#        props.set_fixed_size(self)
        self.win.requestProperties(props)

        self.root = root
        self.x_minus = x_minus
        self.x_plus = x_plus
        self.y_minus = y_minus
        self.y_plus = y_plus

        repeater_m1 = Repeater('mouse1', 0.02)
        repeater_m3 = Repeater('mouse3', 0.02)

        self.scene = None
        if gv.is_debug_mode:
            self.scene = self.set_sceen()

        self.setBackgroundColor(gv.background_color)


        self.f_node_path = self.render.attachNewNode(f_plane_node)
        self.z_scale = 1
        self.is_show_help = False

        self.z_scale_header = OnscreenText(text='z scale', fg=gv.widget_header_color,
                                           pos=(gv.widget_col_left+0*gv.widget_col_size, gv.widget_header_row), scale=gv.widget_text_scale)
        self.z_scale_value = OnscreenText(text=str(self.z_scale), fg=gv.widget_value_color,
                                          pos=(gv.widget_col_left+0*gv.widget_col_size, gv.widget_header_row-1*gv.widget_row_height), scale=gv.widget_text_scale)
        self.resolution_header = OnscreenText(text='Resolution', fg=gv.widget_header_color,
                                              pos=(gv.widget_col_left+1*gv.widget_col_size, gv.widget_header_row), scale=gv.widget_text_scale)
        self.resolution_value = OnscreenText(text=str(gv.points_in_list), fg=gv.widget_value_color,
                                             pos=(gv.widget_col_left+1*gv.widget_col_size, gv.widget_header_row-1*gv.widget_row_height), scale=gv.widget_text_scale)
        self.infi_header = OnscreenText(text='Infinity', fg=gv.widget_header_color,
                                        pos=(gv.widget_col_left+2*gv.widget_col_size, gv.widget_header_row), scale=gv.widget_text_scale)
        self.infi_value = OnscreenText(text=str(gv.INFINITY), fg=gv.widget_value_color,
                                       pos=(gv.widget_col_left+2*gv.widget_col_size, gv.widget_header_row-1*gv.widget_row_height), scale=gv.widget_text_scale)
        self.help_header = OnscreenText(text='help: h', fg=gv.widget_header_color,
                                        pos=(gv.widget_row_right_pos, gv.widget_header_row), scale=gv.widget_text_scale)
        self.help_value = OnscreenText(text='', fg=gv.widget_header_color, pos=(gv.widget_help_col, gv.widget_help_row),
                                       scale=gv.widget_text_scale, align=TextNode.ALeft)

        # enable my camera control
        ShowBase.disableMouse(self)

        # define the camera position with Radius Teta Fi coordinates
        self.reset_cam_pos()

        # handle events
        self.accept('arrow_up', self.move_cam_up)
        self.accept('arrow_up-repeat', self.move_cam_up)
        self.accept('arrow_down', self.move_cam_down)
        self.accept('arrow_down-repeat', self.move_cam_down)
        self.accept('mouse3', self.move_cam_right)
        self.accept('mouse3-repeat', self.move_cam_right)
        self.accept('arrow_right', self.move_cam_right)
        self.accept('arrow_right-repeat', self.move_cam_right)
        self.accept('mouse1', self.move_cam_left)
        self.accept('mouse1-repeat', self.move_cam_left)
        self.accept('arrow_left', self.move_cam_left)
        self.accept('arrow_left-repeat', self.move_cam_left)
        self.accept('wheel_up', self.zoom_in)
        self.accept('j', self.zoom_in)
        self.accept('j-repeat', self.zoom_in)
        self.accept('insert', self.zoom_in)
        self.accept('insert-repeat', self.zoom_in)
        self.accept('wheel_down', self.zoom_out)
        self.accept('m', self.zoom_out)
        self.accept('m-repeat', self.zoom_out)
        self.accept('delete', self.zoom_out)
        self.accept('delete-repeat', self.zoom_out)
        self.accept('4', self.move_down_x)
        self.accept('4-repeat', self.move_down_x)
        self.accept('6', self.move_up_x)
        self.accept('6-repeat', self.move_up_x)
        self.accept('2', self.move_down_y)
        self.accept('2-repeat', self.move_down_y)
        self.accept('8', self.move_up_y)
        self.accept('8-repeat', self.move_up_y)
        self.accept('page_down', self.move_down_z)
        self.accept('page_down-repeat', self.move_down_z)
        self.accept('page_up', self.move_up_z)
        self.accept('page_up-repeat', self.move_up_z)
        self.accept('l', self.move_down_z)
        self.accept('l-repeat', self.move_down_z)
        self.accept('o', self.move_up_z)
        self.accept('o-repeat', self.move_up_z)
        self.accept('0', self.reset_pos_00)
        self.accept('5', self.reset_pos_00)
        self.accept('a', self.scale_up_z)
        self.accept('a-repeat', self.scale_up_z)
        self.accept('z', self.scale_down_z)
        self.accept('z-repeat', self.scale_down_z)
        self.accept('s', lambda: self.change_resolution(12/10))
        self.accept('x', lambda: self.change_resolution(10/12))
        self.accept('d', lambda: self.change_infinity(2))
        self.accept('c', lambda: self.change_infinity(0.5))
        self.accept('h', self.toggle_help)
        self.accept('escape', self.hide_help)

    def set_sceen(self):
        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

    # set x y z position out of r t f with self.offset (default = 0)
    # set heading and pitch to keep sight on (0, 0, 0)
    def set_cam(self):
        x, y, z = self.cam_pos_rtf.get_xyz()
        x += self.cam_offset.x
        y += self.cam_offset.y
        z += self.cam_offset.z
        self.camera.setPos(x, y, z)
        self.camera.setHpr(180-self.cam_pos_rtf.t, -self.cam_pos_rtf.f, 0)

    def reset_pos_00(self):
        self.f_node_path.setPos(0, 0, 0)
        self.z_scale = 1
        self.f_node_path.setSz(self.z_scale)
        self.reset_cam_pos()
        self.set_on_screen_text()

    def reset_cam_pos(self):
        self.cam_pos_rtf = PointRtf(4*gv.DEFAULT_3D_AXE, 160, 20)
        self.cam_offset = Point3D(0, 0, 0)
        self.set_cam()

    def set_on_screen_text(self):
        self.infi_value.text = str(gv.INFINITY)
        self.resolution_value.text = str(gv.points_in_list)
        scale = self.z_scale
        if scale < 1:
            scale = round(scale, 3)
        elif scale < 10:
            scale = round(scale, 1)
        else:
            scale = int(scale)
        self.z_scale_value.text = str(scale)

    def move_down_x(self):
        x = self.f_node_path.getX()
        self.f_node_path.setX(x-gv.DEFAULT_3D_AXE/10)

    def move_up_x(self):
        x = self.f_node_path.getX()
        self.f_node_path.setX(x+gv.DEFAULT_3D_AXE/10)

    def move_down_y(self):
        y = self.f_node_path.getY()
        self.f_node_path.setY(y-gv.DEFAULT_3D_AXE/10)

    def move_up_y(self):
        y = self.f_node_path.getY()
        self.f_node_path.setY(y+gv.DEFAULT_3D_AXE/10)

    def move_down_z(self):
        z = self.f_node_path.getZ()
        self.f_node_path.setZ(z-gv.DEFAULT_3D_AXE/10)

    def move_up_z(self):
        z = self.f_node_path.getZ()
        self.f_node_path.setZ(z+gv.DEFAULT_3D_AXE/10)

    def move_cam_up(self):
        self.cam_pos_rtf.f += 2
        self.set_cam()

    def move_cam_down(self):
        self.cam_pos_rtf.f -= 2
        self.set_cam()

    def move_cam_right(self):
        self.cam_pos_rtf.t -= 2
        self.set_cam()

    def move_cam_left(self):
        self.cam_pos_rtf.t += 2
        self.set_cam()

    def zoom_in(self):
        if self.cam_pos_rtf.r > 0:
            self.cam_pos_rtf.r *= 9/10
            self.set_cam()

    def zoom_out(self):
        self.cam_pos_rtf.r *= 10/9
        self.set_cam()

    def scale_down_z(self):
        self.z_scale *= 10/12
        self.f_node_path.setSz(self.z_scale)
        self.set_on_screen_text()

    def scale_up_z(self):
        self.z_scale *= 12/10
        self.f_node_path.setSz(self.z_scale)
        self.set_on_screen_text()

    def change_resolution(self, f):
        self.f_node_path.removeNode()
        gv.points_in_list = int(gv.points_in_list * f)
        v_matrix, list_x, list_y = get_3D_matrix(self.root, self.x_minus, self.x_plus, self.y_minus, self.y_plus)
        node = get_f_plane_node(v_matrix, list_x, list_y)
        self.f_node_path = self.render.attachNewNode(node)
        self.set_on_screen_text()


    def change_infinity(self, f):
        self.f_node_path.removeNode()
        gv.INFINITY = int(gv.INFINITY * f)
        v_matrix, list_x, list_y = get_3D_matrix(self.root, self.x_minus, self.x_plus, self.y_minus, self.y_plus)
        node = get_f_plane_node(v_matrix, list_x, list_y)
        self.f_node_path = self.render.attachNewNode(node)
        self.set_on_screen_text()

    def toggle_help(self):
        if self.is_show_help:
            self.hide_help()
        else:
            self.show_help()

    def hide_help(self):
        self.help_value.text = ''
        self.is_show_help = False

    def show_help(self):
        help_header = """
        use arrows + mouse buttons and wheel


        move-x       move-y           move-z              reset position
           4-6                 2-8          Page Up-Down               5


        z-scale     resolution    infinity limit       zoom in-out
           a-z               s-x                 d-c                Insert-Delete
        """
        self.help_value.text = help_header
        self.is_show_help = True


