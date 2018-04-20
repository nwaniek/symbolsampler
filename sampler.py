#!/usr/bin/env python3

import os, sys
import numpy as np


from primitives import *
from scenes import *


class Agent:
    pass



aabox = AABox(np.array([0.0, 0.0, 0.0]), np.array([1.0, 1.0, 0.0]))
cyl = Cylinder(np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 1.0]), 1.0)


tri = Triangle(np.array([0.0, 0.0, 0.0]),
               np.array([1.0, 0.0, 0.0]),
               np.array([0.5, 0.0, 0.5]))

wall = Wall(np.array([0.0, 0.0, 0.0]),
            np.array([1.0, 0.0, 0.0]),
            0.5)

ray = Ray(np.array([0.5, 0.5, 0.1]),
          np.array([0.0, -0.1, 0.0]))

print(aabox.intersect(ray))
