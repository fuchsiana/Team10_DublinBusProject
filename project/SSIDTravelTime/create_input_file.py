import pandas as pd
import numpy as np
import csv
import feather
import pickle



def create_base_on_route():
    
    res = pd.read_feather('DBus_stage_two_clean_v4.feather')
    res['route'] = res['JourneyPatternID'].str[:4]
    if 'level_0' in res.columns:
        res.drop('level_0', axis=1, inplace=True)
    route_list = res.route.unique()
    for r in route_list:
        print(r)
        temp = res[res.route == r]
        filename = 'route' + str(r) + '.feather'
        temp = temp.reset_index()
        temp.to_feather(filename)
        del temp
        
def create_route_list():
    res = pd.read_feather('DBus_stage_two_clean_v4.feather')
    res['route'] = res['JourneyPatternID'].str[:4]
    route_list = res.route.unique()
    print(route_list)
    pickle_temp = open('input3_routs_list.pkl', 'wb')
    pickle.dump(route_list, pickle_temp)
    pickle_temp.close()



if __name__ == '__main__':
    create_route_list()