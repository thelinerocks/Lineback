import numpy as np
import random
import matplotlib.pyplot as plt
from database import *

class make_data(object):
    def __init__(self):
        self.old_val = 0
        self.new_val = 0

    def add_steps(self,data):
        size = int(1/0.05)
        total_array = np.zeros(size)
        for i in range(size):
            total_array[i] = (data[0]) + ((data[1]-data[0])/size)*i
        return total_array

    def get_ticks(self,category):
        total = get_sum_text(category) + get_sum_image(category)
        old_total = 2
        return self.add_steps([old_total,total])


md = make_data()
md.get_ticks()


