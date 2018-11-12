#!/usr/pkg/bin/env python
#

from sympy import ImageSet, S, Lambda
from sympy.abc import *

def square(x):
	squares = ImageSet(Lambda, x), S.Naturals)
