import time;
import numpy as np
import json
from picture_classifier import *

hours = np.zeros(24)
secs = np.zeros(60)
mins = np.zeros(60)



def add_value():
    min_index = 0
    hours_index = 0
    secs_index = 0

    with open('details.json', 'r') as file:
        data = json.load(file)
    get_photo_happiness(data)


    localtime = time.localtime(time.time())
    if(localtime.tm_hour > hours[hours_index]):
        hours_index = (hours_index + 1)%24
        hours[hours_index] =
    if(localtime.tm_min):
        min_index = (min_index + 1)%60


    if(localtime.tm_sec):
        print("Hellos")
localtime = time.localtime(time.time())
print("Local current time :" +  str(localtime))

