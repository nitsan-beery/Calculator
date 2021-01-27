from panda3d import core
import global_vars as gv


def get_f_plane_node(v_matrix, list_x, list_y):
    format = core.GeomVertexFormat.get_v3c4()
    vdata = core.GeomVertexData('name', format, core.Geom.UHStatic)
    vertex = core.GeomVertexWriter(vdata, 'vertex')
    color = core.GeomVertexWriter(vdata, 'color')
    geom = core.Geom(vdata)
    node = core.GeomNode('f_node')

    num_vertices = 0
    for row in v_matrix:
        num_vertices += len(row)
    # vertices in f_plane + 3 axes
    vdata.setNumRows(num_vertices+6)


    add_vertices(v_matrix, vertex, color)
    add_lines(list_x, geom)
    add_lines(list_y, geom)
    add_axes(num_vertices, vertex, color, geom)

    node.addGeom(geom)

    return node


def add_vertices(v_matrix, vertex, color):
    for row in range(len(v_matrix)):
        for col in range(len(v_matrix[row])):
            p = v_matrix[row][col]
            vertex.addData3(p.x, p.y, p.z)
            color.addData3(gv.line_color)


def add_lines(list, geom):
    for line in list:
        prim = core.GeomLinestrips(core.Geom.UHStatic)
        if len(line) > 1:
            for v in line:
                prim.addVertex(v)
            try:
                prim.close_primitive()
                geom.addPrimitive(prim)
            except:
                print(f'DEBUG: exception adding line {line}')


def add_axes(start_vertex, vertex, color, geom):
    # x axe
    prim = core.GeomLines(core.Geom.UHStatic)
    vertex.addData3(-gv.DEFAULT_3D_AXE, 0, 0)
    color.addData3(gv.axe_color)
    vertex.addData3(gv.DEFAULT_3D_AXE, 0, 0)
    color.addData3(gv.axe_color)
    prim.add_consecutive_vertices(start_vertex, 2)
    start_vertex += 2
    prim.close_primitive()
    geom.addPrimitive(prim)

    # y axe
    prim = core.GeomLines(core.Geom.UHStatic)
    vertex.addData3(0, -gv.DEFAULT_3D_AXE, 0)
    color.addData3(gv.axe_color)
    vertex.addData3(0, gv.DEFAULT_3D_AXE, 0)
    color.addData3(gv.axe_color)
    prim.add_consecutive_vertices(start_vertex, 2)
    start_vertex += 2
    prim.close_primitive()
    geom.addPrimitive(prim)

    # z axe
    prim = core.GeomLines(core.Geom.UHStatic)
    vertex.addData3(0, 0, -gv.DEFAULT_3D_AXE)
    color.addData3(gv.z_axe_color)
    vertex.addData3(0, 0, gv.DEFAULT_3D_AXE)
    color.addData3(gv.z_axe_color)
    prim.add_consecutive_vertices(start_vertex, 2)
    start_vertex += 2
    prim.close_primitive()
    geom.addPrimitive(prim)

