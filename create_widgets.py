from panda3d import core
import global_vars as gv


def get_widgets_node():
    format = core.GeomVertexFormat.get_v3()
    vdata = core.GeomVertexData('name', format, core.Geom.UHStatic)
    vertex = core.GeomVertexWriter(vdata, 'vertex')
    geom = core.Geom(vdata)
    node = core.GeomNode('widget_node')

    return node

