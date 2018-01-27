import numpy as np
import pandas as pd
from random import randint

def get_random_url():
    dataset = pd.read_csv("Pictures.txt", delimiter="\n", header=None)
    dataset = np.array(dataset)

    number_of_links = (dataset.shape[0]) - 1
    random_index = (randint (0,number_of_links))
    return(dataset[random_index][0][:-1])

