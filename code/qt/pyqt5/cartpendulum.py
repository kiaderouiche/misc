#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
original problem:
I am trying to understand the force present in the system below. I found this picture online 
and I would like to ask what is the force N and P of the cart and Pendulum for? I tried to google it but i am not really sure what is the term of this force called and not much result is found for this 2 force.
May I seek some help on
understanding the force N and P , what is their purpose and why is it present?
enter image description here
# https://physics.stackexchange.com/questions/375790/what-is-the-force-n-and-p-of-the-cart-and-pendulum-for 
 
 
 
  |                     |
  |                     |
  |                     |
  |---------------------|
  
----------------------------

"""

import sys

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLineEdit, QSpinBox,
                             QStyleFactory, QWidget)

from sympy import symbols
from sympy.physics.mechanics import *

if __name__ == '__main__':
	print('Calculation N and P force')
