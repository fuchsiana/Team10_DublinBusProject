import pandas as pd
import numpy as np
import csv
import feather
import pickle
import time


def create_base_on_route():
    
    res = pd.read_feather('DBus_stage_two_clean_v4.feather')
# here create list containing all required route feather files
    res['route'] = res['JourneyPatternID'].str[:4]
    route_list = ['put', 'in', 'all', 'routes', 'you','want','a', 'feather', 'file', 'for', 'e.g.', '046A']
    for r in route_list:
        print(r)
        tp1 = time.time()
        temp = res[res.route == r]
        filename = 'route' + str(r) + '.feather'
        temp = temp.reset_index()
        temp.to_feather(filename)
        print("Time for", r, ":", int(time.time() - tp1))
        del temp




if __name__ == '__main__':
    create_base_on_route()