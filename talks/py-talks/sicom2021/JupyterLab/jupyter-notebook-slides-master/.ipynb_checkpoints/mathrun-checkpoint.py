from sympy.abc import *
from sympy import init_printing, symbols, Symbol
from sympy import expand, factor, collect

init_printing(pretty_print=True)

def affichePol():
    P = y*x**2 - x**4 + y**5
    return P

def calInPol(affichePol):
    l = affichePol()
    print(l)

if __name__ == "__main__":
   affichePol()