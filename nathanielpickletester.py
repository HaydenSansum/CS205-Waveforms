import numpy as np 
import pandas as pd
import sparkpickle

with open("nathaniel.pkl/part-00000.pkl", "rb") as f:
    for obj in sparkpickle.load_gen(f):
        print(obj)

# with open("nathaniel.pkl/part-00000.pkl", "rb") as f:
#     print(sparkpickle.load(f))