from geopy.distance import great_circle
from datetime import datetime
import pandas as pd
import numpy as np
import feather
import csv
import os
import pickle

## --------------- Revised record ----------------- ##
# 11.07 due to memory shortage, try del dataframe and append to csv directly

def main(filename):
    
    # Share memory of dataframe
    global gps
    global stop_loc
    
    # Share memory of result
    global gps_res
    global travel_time_res
    
    # Read input file (Function 1.0)
    gps, stop_loc = read_file(filename)
    print('Read file finished.')
    
    # Get list of group that key is 'TimeFrame', 'JourneyPatternID', 'VehicleJourneyID' (Function 1.1)
    unique_key = get_group_list()
    print('Get unique key finished.')
    
    # Initialize before loop
    current_route = unique_key[0][0][:4]
    gps_res = gps[(gps.TimeFrame == '2013-1-32')] # For keep the datatype
    travel_time_res = pd.DataFrame(columns=['JourneyPatternID', 'TimeFrame', 'SSID', 'SourceStopID', 'DestStopID', 'Day', 'HourFrame', 'TravelTime', 'WindSpeed', 'Rain', 'SchoolHoliday'])
    
    print(current_route)
    
    # Calculate group by group and write to file route by route
    for key in unique_key:
        print('Key:', key)
        # Write data into separate route file
        if key[0][:4] != current_route or key == unique_key[-1]:
            print(str(current_route) + ' write to file finished.')
            # Write row to keep and traveling time between stops result to feather file
            gps_res = gps_res.reset_index()
            gps_res.to_feather('Route_' + str(current_route) + '_after.feather')
            travel_time_res.to_csv('Route_' + str(current_route) + '_travel_time.csv', index=False)
            
            # Clean up
            del gps_res
            del travel_time_res
            
            # Initialize
            gps_res = pd.DataFrame(columns=gps.columns)
            travel_time_res = pd.DataFrame(columns=['JourneyPatternID', 'TimeFrame', 'VehicleJourneyID', 'SourceStopID', 'DestStopID', 'SSID', 'Day', 'HourFrame', 'TravelTime', 'WindSpeed', 'Rain', 'SchoolHoliday'])

            # Update current route
            current_route = key[0][:4]
        
        # Get sub-dataframe base on the key
        gps_sub = gps[(gps.JourneyPatternID == key[0]) & (gps.TimeFrame == key[1]) & (gps.VehicleJourneyID == key[2])]
        
        # Get index of sub-dataframe that should keep. (Function 1.2)
        idx_to_keep = get_index_of_row_to_keep(gps_sub)
        
        # Get the traveling time between two stops. (Function 1.3)
        travel_time_df = calculate_time_between_stops(key, idx_to_keep)
        
        # Concate result before write to feather file (Function 1.4)
        concat_result(idx_to_keep, travel_time_df)
        
        
        
def read_file(filename):
    """ 1.0 Read required data and prepare data"""    
    
    gps_filename = filename
    stop_location_filename = 'input1_StopID_LonLat.csv'

    gps = pd.read_feather(gps_filename)
    #gps = pd.read_csv(gps_filename)
    stop = pd.read_csv(stop_location_filename)
    
    # Prepare
    if 'level_0' in gps.columns:
        gps.drop('level_0', axis=1, inplace=True)
    
    
    #gps.drop(['index','Delay','VehicleID'], axis=1, inplace=True)
    
    gps['TimeFrame'] = gps['TimeFrame'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))
    gps.sort_values('JourneyPatternID', inplace=True)
    gps['Index'] = gps.index
    
    
    stop.StopID = stop.StopID.apply(lambda x: str(int(x)).zfill(4))
    stop.set_index('StopID', inplace=True)
    stop = stop.to_dict('index')
    
    return gps, stop

def get_group_list():
    """ 1.1 Return the list of key that is group by 'TimeFrame', 'JourneyPatternID', 'VehicleJourneyID' """
    
    global gps
    
    # Order by JourneyPatternID (for the purpose to store to different file later
    gb = gps.groupby(['JourneyPatternID', 'TimeFrame', 'VehicleJourneyID'])
    group = pd.DataFrame(gb['AtStop'].count())
    print()
    group.reset_index(['JourneyPatternID', 'TimeFrame', 'VehicleJourneyID'], inplace=True)
    
    list = []
    for i in group.index:
        temp = [group.iloc[i]['JourneyPatternID'], group.iloc[i]['TimeFrame'], group.iloc[i]['VehicleJourneyID']]
        list.append(temp)
    
    return list


## ------------------ Start 1.2: Get index of row to keep ---------------------- ##

def concat_result(idx, travel_time_df):
    """Concat dataframe to result dataframe"""
    
    global gps
    global gps_res
    global travel_time_res
    
    gps_res = pd.concat([gps_res, gps[gps.Index.isin(idx)]], axis=0)
    travel_time_res = pd.concat([travel_time_res, travel_time_df], axis=0)
    return
    
## ------------- 1.2 Start: Get index of row to keep ------------- ##

def get_index_of_row_to_keep(gps_sub):
    """1.2 return the index of row that should keep for later to calculate time between two stops.
    
    Input parameter will be a dictionary with keys corresponding to the columns name 
    and the StopID corresponding to its Lon/Lat."""
    
    global gps_sub_dict
    global stop_loc
    global gps

    index_of_row_to_keep = []
    
    # -------- 1. sort by Timestamp --------------- #
    gps_sub['Timestamp'] = pd.to_datetime(gps_sub['Timestamp'], format='%Y-%m-%d %H:%M:%S')
    gps_sub.sort_values('Timestamp', inplace=True)
    # Use dict to work on the rest of the work
    gps_sub_dict = gps_sub.to_dict('list')
    
    #-------- 2. iterate on each row --------------- #
    flag = gps_sub_dict['StopID'][0]
    for i in range(len(gps_sub_dict['Index'])):
        # if is first stop append index with max Timeframe in index_of_row_to_keep
        if is_first_stop(i):
            if is_near_stop(i) and not is_next_row_same_stopID(i):
                index_of_row_to_keep.append(gps_sub_dict['Index'][i])
        
        # if not the first bus stop, should keep the row with min Timestamp that is nearest the bus stop
        else:
            # so if near the bus stop and that bus stop hasn't mark any row to keep
            if is_near_stop(i) and gps_sub_dict['StopID'][i] != flag:
                index_of_row_to_keep.append(gps_sub_dict['Index'][i])
                flag = gps_sub_dict['StopID'][i]

    return index_of_row_to_keep
   
def get_first_stop():
    """return StopID of the first stop"""  
    
    global gps_sub_dict
    
    return gps_sub_dict['StopID'][0]

def is_first_stop(i):
    """return true if the StopID of this row is the first Stop
    
    i indicate row i"""
    
    global gps_sub_dict
    
    return gps_sub_dict['StopID'][i] == get_first_stop()
     
def distance_to_stop(i):
    """return the distance to the stop"""
    
    global gps_sub_dict
    global stop_loc
    global gps
    
    if is_next_row_same_stopID(i):
        return distance_to_self_stop(i)
    else:
        # Here also need to check if self(i) is closer or next row(i+1) is closer.
        # If the minimal one is self not next row, need to replace the self StopID to next StopID
        
        # if distance_to_next_stop(i) < distance_to_self_stop(i) and distance_to_next_stop(i) < distance_to_self_stop(i+1):
        if distance_to_next_stop(i) < distance_to_self_stop(i+1):
            idx = gps[gps.Index == gps_sub_dict['Index'][i]].index
            gps.loc[idx, 'StopID'] = gps_sub_dict['StopID'][i+1]
            
            gps_sub_dict['StopID'][i] = gps_sub_dict['StopID'][i+1]
            
            return distance_to_next_stop(i)
        else:
            return distance_to_self_stop(i)
    
def distance_to_self_stop(i):
    """return the distance to the StopID itself"""
    
    global gps_sub_dict
    global stop_loc
    
    stopID = gps_sub_dict['StopID'][i]
    gps_position = (gps_sub_dict['Lat'][i], gps_sub_dict['Lon'][i])
    stop_position = (stop_loc[stopID]['Lat'], stop_loc[stopID]['Lon'])
    
    return great_circle(gps_position, stop_position).meters
    
def distance_to_next_stop(i):
    """return the distance to the StopID of next row"""
    
    global gps_sub_dict
    global stop_loc
    
    if i < len(gps_sub_dict['StopID'])-1:
        stopID = gps_sub_dict['StopID'][i+1]
        gps_position = (gps_sub_dict['Lat'][i], gps_sub_dict['Lon'][i])
        stop_position = (stop_loc[stopID]['Lat'], stop_loc[stopID]['Lon'])
        return great_circle(gps_position, stop_position).meters
    else:
        return distance_to_self_stop(i)
     
def is_next_row_same_stopID(i):
    """return true if next the StopID of next row doesn't change"""
    
    global gps_sub_dict
    
    if i < len(gps_sub_dict['StopID'])-1:
        return gps_sub_dict['StopID'][i] == gps_sub_dict['StopID'][i+1]
    else:
        return True
    
def is_near_stop(i):
    """return true if the position of the row is near stop"""
    
    global gps_sub_dict
    global stop_loc
    
    # If is near stop > number need to tune
    return distance_to_stop(i) < 300


## ------------- 1.2 End: Get index of row to keep ------------- ## 

def calculate_time_between_stops(key, idx):
    """ 1.3 Get the traveling time between two stops"""
    
    global gps
    
    gps_sub = gps[gps.Index.isin(idx)]

    # first make sure sorted by timestamp
    gps_sub.sort_values('Timestamp', inplace=True)
    
    #print(dfSubGroup.info())
    df_time_diff = pd.DataFrame(columns=['JourneyPatternID', 'TimeFrame', 'SourceStopID', 'DestStopID', 'SSID', 'Day', 'HourFrame', 'TravelTime', 'WindSpeed', 'Rain', 'SchoolHoliday'])

    for i in range(len(gps_sub) -1):
        dfTemp = pd.DataFrame([gps_sub[['JourneyPatternID', 'TimeFrame', 'VehicleJourneyID', 'Day', 'SchoolHoliday']].iloc[i]], columns= ['JourneyPatternID', 'TimeFrame', 'VehicleJourneyID', 'Day', 'SchoolHoliday'])
        dfTemp['WindSpeed'] = gps_sub['Wind_Speed_Avg'].iloc[i]
        dfTemp['Rain'] = gps_sub['Rain_Avg'].iloc[i]
        dfTemp['SourceStopID'] = str(gps_sub['StopID'].iloc[i]) 
        dfTemp['DestStopID'] = str(gps_sub['StopID'].iloc[i+1])
        dfTemp['SSID'] = str(gps_sub['StopID'].iloc[i]) + str(gps_sub['StopID'].iloc[i+1])
        dfTemp['TravelTime'] = (gps_sub['Timestamp'].iloc[i+1] - gps_sub['Timestamp'].iloc[i]).seconds
        dfTemp['HourFrame'] = gps_sub['Timestamp'].iloc[i].hour
        
        df_time_diff = df_time_diff.append(dfTemp)
    
    return df_time_diff


if __name__ == '__main__':
    
    # --------------------- Emma --------------------- #
    route_list = ['0007', '0083', '0102', '0039', '0014', '0041', '0016', '0037', '0015', '0067',\
                  '0027', '046A', '0747', '0013', '033B', '0018', '040D', '045A', '041C', '0184',\
                  '0145', '0033', '0123', '0047', '0059', '065B', '0009', '0069', '066A', '0049']
    for route in route_list:
        file = 'input2_routes/route' + route + '.feather'
        main(file)
        print('Route: ' + route + ' done!')
    print('Done! :)')
    
    # --------------------- Willi --------------------- #
    route_list = ['077A', '066B', '0063', '016C', '025A', '0040', '0032', '015A', '056A', '0150',\
                  '0044', '054A', '0017', '0070', '0038', '0011', '0066', '025B', '039A', '0025',\
                  '0122', '041B', '0076', '0151', '0043', '0061', '017A', '084A', '027A', '0140']
    for route in route_list:
        file = 'input2_routes/route' + route + '.feather'
        main(file)
        print('Route: ' + route + ' done!')
    print('Done! :)')
    
    # --------------------- Ian --------------------- #
    route_list = ['0120', '068A', '0004', '0001', '0239', '015B', '0065', '0270', '007B', '0130',\
                  '040B', '0079', '044B', '0026', '076A', '038B', '027B', '0053', '0008', '0220',\
                  '0104', '079A', '084X', '0031', '0114', '007D', '0142', '041X', '0238', '027X']
    for route in route_list:
        file = 'input2_routes/route' + route + '.feather'
        main(file)
        print('Route: ' + route + ' done!')
    print('Done! :)')
    
    # --------------------- Wen-Ting --------------------- #
    route_list = ['046E', '0068', '038A', '031A', '083A', '0084', '0185', '066X', '069X', '031B',\
                  '0236', '029A', '0042', '0075', '033X', '041A', '067X', '032X', '051D', '0111',\
                  '051X', '0116', '0161', '0118', '025X', '033A', '014C']
    for route in route_list:
        file = 'input2_routes/route' + route + '.feather'
        main(file)
        print('Route: ' + route + ' done!')
    print('Done! :)')
    
    
    
