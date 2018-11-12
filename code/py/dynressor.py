#!/usr/bin/env python2
#
"""
Usage

       -------->  x, v
                                     
|    k   ------            
|-/\--/\-| m  |--> F   | g
|        ------        V
-------------------

"""

# Derive the system

from sympy import init_printing
from sympy import symbols
from sympy.physics.mechanics import *

init_printing(pretty_print=True)

m, g, d, stiffness = symbols('m g d stiffness')
position, speed = dynamicsymbols('x v')
positiond = dynamicsymbols('x', 1)
force = dynamicsymbols('F')

ceiling = ReferenceFrame('N')

origin = Point('origin')
origin.set_vel(ceiling, 0)

center = origin.locatenew('center', position*ceiling.x)
center.set_vel(ceiling, speed*ceiling.x)

block = Particle('block', center, m)

kinematic_equations = [speed - positiond]

force_magnitude = m*g - stiffness*position-d*speed+force
forces = [(center, force_magnitude*ceiling.x)]

particles = [block]

kane = KanesMethod(ceiling, q_ind=[position], u_ind=[speed],
	kd_eqs=kinematic_equations)

kane.kanes_equations(forces, particles)