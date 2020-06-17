# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:46:01 2020

Chamber function tools

@author: J Kodros
"""

import numpy as np



# Wall loss 
def first_order_loss_func(x, a, c, d):
    return a*np.exp(-c*(x-d))

