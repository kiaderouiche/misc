# IPython log file

get_ipython().run_line_magic('logstart', '')
#Lancer l'engirsement de la session
get_ipython().run_line_magic('logstart', '')
get_ipython().run_line_magic('logstat', '')
get_ipython().run_line_magic('logstate', '')
# Multimedia 
import json
get_ipython().run_line_magic('pinfo', 'json')
import os.path
get_ipython().run_line_magic('pinfo2', 'os.path')
import io
import io
get_ipython().run_line_magic('pinfo', 'io')
import io
get_ipython().run_line_magic('pinfo', 'io.BytesIO')
import io
get_ipython().run_line_magic('pinfo', 'io.BytesIO')
get_ipython().system(' du -h /etc')
Avec le notebook  du Jupyter on a :
    - accés à tous les services noyau de IPython y compris l'affichage riche des objets
    - la possibilité d'inser
#Demo de ipywidgts
def demo(ok, entier, flottant, texte, code):
    return "ok={}, entier={}; flottant={}; texte={}, code={}".format(ok, entier, flottant, texte, code)
#Demo de ipywidgts
def demo(ok, entier, flottant, texte, code):
    return "ok={}, entier={}; flottant={}; texte={}, code={}".format(ok, entier, flottant, texte, code)
interact(demo, ok=True, entier=(1, 10), flottant=(0.0, 1.0), texte=('pomme', 'poire', 'orange'),
        code=('clef1':'premiére clé', 'clef2':'deuxiéme clé'))
#Demo de ipywidgts
def demo(ok, entier, flottant, texte, code):
    return "ok={}, entier={}; flottant={}; texte={}, code={}".format(ok, entier, flottant, texte, code)
interact(demo, ok=True, entier=(1, 10), flottant=(0.0, 1.0), texte=('pomme', 'poire', 'orange'),
        code={'clef1':'premiére clé', 'clef2':'deuxiéme clé'})
import pandas as pd
import numpy as np
