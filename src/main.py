# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 21:39:20 2019

@author: Satya
"""

from Solver import *
import sys

if __name__ == "__main__":
    if not(len(sys.argv)==3):
        raise Exception('Wrong command line arguments')
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    obj = Solver()
    obj.read(input_file)
    obj.process()
    obj.solve()
    obj.write(output_file)