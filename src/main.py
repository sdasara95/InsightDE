# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 21:39:20 2019

@author: Satya
"""

import Solver.Solver as solver
import sys

if __name__ == "__main__":
    if not(len(sys.argv)==3):
        raise Exception('Wrong command line arguments')
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    obj = solver()
    obj.read(input_file)
    obj.process()
    obj.write(output_file)