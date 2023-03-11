import pprint
import os

def function_x(**kwargs): 
    pprint.pprint(list(os.environ.items()))
    return