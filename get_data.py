import numpy as np
import random
import matplotlib.pyplot as plt
import database

class make_data(object):
    def __init__(self):
        self.old_val = 0
        self.new_val = 0

    def smooth(self,y, box_pts):
        box = np.ones(box_pts)/box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    def add_steps(self,data,timesteps):
        size = 1/0.05
        total_array = np.zeros(size)
        c = 0
        for i in range(size):
            total_array[i] = (data[i]) + (data[i+1])



