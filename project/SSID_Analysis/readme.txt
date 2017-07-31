get_stops_sequence_by_googletransit.ipynb requires stop_times.csv and trips.csv from the zip here: https://github.com/wjdelaney/Team-10/blob/master/project/DataAnalytics/supplemental_data_files/googletransitdbfeedp20121129-1547.zip

Please copy these three files into a local folder to run.

---------------------------

Analysis_of_SSID_Template.ipynb requires the Route_XXXX_travel_time.csv for every route that traverses the SSID (list produced by get_stops_sequence_by_googletransit.ipynb) to be in the same folder; please copy these files into a local folder to run. 

Analysis_of_SSID_XXXXXXXX.ipynb requires either the above listed Route_XXXX_travel_time.csv files, or the file can be run from the SSID_XXXXXXXX.csv file (if one is contained in the SSID_CSVs folder) by changing the SSID_XXXXXXXX.csv filename in cell 12, and then running the notebook from that cell (after the imports in cell one).