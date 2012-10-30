from pygamehelper import *
from pygame import *
from pygame.locals import *

from vec import vec2d

from math import e, pi, cos, sin, sqrt
from random import uniform, randint

class Animation(PygameHelper):

    def __init__(self, w, h):
    
        self.w = w
        self.h = h
        
        PygameHelper.__init__(self, size=(self.w, self.h), fill=((255,255,255)))

    #pygame
    def update(self):
        pass
                
    def keyUp(self, key):
        pass



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-W", type=int, help="Width of window", default=1300)
    parser.add_argument("-H", type=int, help="Height of window", default=800)
    args = parser.parse_args()
    
    s = Animation(args.W, args.H)
    s.mainLoop(60)