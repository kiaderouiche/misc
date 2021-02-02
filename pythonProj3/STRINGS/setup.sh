#!/bin/bash

# An example to set up the environment variables to use PDF sets of the LHAPDF
# It should be sourced before using the program
# Authors: Fairhurst Lyons, Pourya Vakilipourtakalou & Douglas Gingrich      Oct 2020
# INSTALLATION_PATH needs to be set to the directory in which the LHAPDF has been installed.

export INSTALLATION_PATH=$HOME/LHAPDF-6.X.Y
export PATH=$INSTALLATION_PATH/bin:$PATH
export LD_LIBRARY_PATH=$INSTALLATION_PATH/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$INSTALLATION_PATH/lib64/python2.7/site-packages:$PYTHONPATH
