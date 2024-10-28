import math
import numpy as np
import pyxel as px

class Curva_bezier:
    def __init__(self,p0,p1,p2,p3):
        self.p0 = np.array(p0)
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        self.p3 = np.array(p3)
        
    def draw(self):
        global t
        t = (px.frame_count / 60) % 1
        x = ((1 - t)**3)*self.p0[0] + (3*t*((1 - t)**2))*self.p1[0] + (3*(t**2)*(1 - t))*self.p2[0] + (t**3)*self.p3[0]
        y = ((1 - t)**3)*self.p0[1] + (3*t*((1 - t)**2))*self.p1[1] + (3*(t**2)*(1 - t))*self.p2[1] + (t**3)*self.p3[1]
        px.circ(x, y, 2, 12)

        d0 = -3*(1 - t)**2 # derivadas
        d1 = 3*t*(2*t - 2) + 3*(1 - t)**2
        d2 = -3*t**2 + 6*t*(1 - t)
        d3 = 3*t**2
        dx = d0*self.p0[0] + d1*self.p1[0] + d2*self.p2[0] + d3*self.p3[0]
        dy = d0*self.p0[1] + d1*self.p1[1] + d2*self.p2[1] + d3*self.p3[1]

        d = math.sqrt(dx*dx + dy*dy)
        px.line(x, y, x + 10*dx/d, y + 10*dy/d, 7)
        px.line(x, y, x - 10*dy/d, y + 10*dx/d, 10)

#cada ponto deverá ser um array contendo o x e o y!
curva1 = Curva_bezier([400,400],[0,0],[400,0],[1,400])
curva2 = Curva_bezier([0,0],[400,400],[0,400],[400,1])

def update():
    pass

def draw():
    curva1.draw()
    curva2.draw()

px.init(400, 400)
px.run(update, draw)
