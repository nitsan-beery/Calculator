import math

class PointRtf:
    def __init__(self, r=0, t=0, f=0):
        self.r = r
        self.t = t
        self.f = f

    def get_xyz(self):
        # convert degrees to radians
        rad = math.pi/180
        r = self.r
        t = self.t * rad
        f = self.f * rad

        d = math.cos(f)*r
        z = math.sin(f)*r
        y = math.cos(t)*d
        x = math.sin(t)*d

        return x, y, z

    def get_x(self):
        x, y, z = self.get_xyz()
        return x

    def get_y(self):
        x, y, z = self.get_xyz()
        return y

    def get_z(self):
        x, y, z = self.get_xyz()
        return z
