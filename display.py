#!/usr/bin/python
# coding: utf-8

from matplotlib import pyplot as plt
from matplotlib import animation, colors

class Display(object):

    def __init__(self, mapa, values, paints, update):
        self.__make_cmap(paints, values)
        self.update = update
        self.__show(mapa)

    def __make_cmap(self, paints, values):
        self.cmap = colors.ListedColormap(paints)
        bounds = []
        for i in xrange(len(values) - 1):
            a = values[i]
            b = values[i+1]
            x = (a+b)/2.
            bounds += [a, x]
        bounds.append(b)
        self.norm = colors.BoundaryNorm(bounds, self.cmap.N)

    def __show(self, mapa):
        self.fig = plt.figure()
        self.im = plt.imshow(mapa, interpolation='nearest', cmap=self.cmap, norm=self.norm)
        self.ani = animation.FuncAnimation(self.fig, self.__updateAnimation, frames=None, interval=20, blit=True)
        plt.axis('off')
        #self.__record()
        plt.show()

    def __updateAnimation(self, *args):
        map = self.update()
        self.im.set_array(map)
        return self.im,

    def __record(self):
        self.ani.save('movie.mp4', fps=15, extra_args=['-vcodec', 'libx264'])
