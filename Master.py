import time
import numpy as np
import json
from picture_classifier import *
from RandomImages import *



class get_values(object):
    def __init__(self):
        self.mins_index = 0
        self.hours_index = 0
        self.secs_index = 0
        self.hours = np.zeros(24)
        self.mins = np.zeros(60)
        self.secs = np.zeros(6)
        self.interval = 10
        self.oldtime = time.localtime(time.time()).tm_sec

    def add_values(self,url):
        while True:
            localtime = time.localtime(time.time())
            data_list = []

            while localtime.tm_sec==self.oldtime or localtime.tm_sec%self.interval != 0:
                url = get_random_url()
                data_list.append(get_data(url))
                localtime = time.localtime(time.time())
            value = sum(data_list)

            self.secs_index = int((self.secs_index+1)%(60/self.interval))
            self.secs[self.secs_index] = value

            if(localtime.tm_hour != self.hours[self.hours_index]):
                self.hours_index = localtime.tm_hour
                self.hours[self.hours_index] = np.sum(self.mins)
            if(localtime.tm_min != self.mins_index):
                self.mins_index = localtime.tm_min
                self.mins[self.mins_index] = np.sum(self.secs)
            self.calculate_value()
            self.oldtime = localtime.tm_sec
            print(self.calculate_value())

    def calculate_value(self):
        value = np.sum(self.hours)*5 + np.sum(self.mins)**1.5 + np.sum(self.secs) ** 2
        return value

gv = get_values()
print(gv.add_values(url = 'https://media1.s-nbcnews.com/j/newscms/2016_30/1639976/160726-keith-weglin-713p_801485078c1d37cb8920b8a779546666.nbcnews-ux-2880-1000.jpg'))