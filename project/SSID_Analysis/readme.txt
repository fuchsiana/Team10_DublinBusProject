Copied from the Wiki

NOTE: Before running these files, copy them to a different folder on your home machine along with any relevant data csv files. Do not move new data files into the GitHub folder, unless you're uploading a new SSID analysis.

If opening an existing SSID analysis:

* Can be viewed in the browser, but please create a copy in Jupyter before making any changes, and keep both versions up on Master.
* Check that the corresponding csv file exists in the SSID_CSVs folders; if it does, you can just load the first cell (imports) and then skip down to the twelfth and 'Cell -> Run All Below' from there.
* Feel free to try out new feature creation or models on any of these, and to add any other SSIDs you do.

If creating a new SSID analysis from template, follows steps in this order:

1. open get_stops_sequence_by_googletransit.ipynb
2. requires stop_times.csv and trips.csv (from the zip here: https://github.com/wjdelaney/Team-10/blob/master/project/DataAnalytics/supplemental_data_files/googletransitdbfeedp20121129-1547.zip) to be in the same folder
3. write required SSID number over 'YOUR_NUMBER_HERE' in bottom cell and run notebook to get the list of routes that traverse this segment. Copy this list.
4. ensure route csv files from Output_SSID_Traveling_Time.py for each route in the list are contained in Route_XXXX_travel_time_csvs folder
5. open Analysis_of_SSID_Template.ipynb
6. paste list over '['list', 'here', 'of', 'all', 'routes', 'required']' in first cell. Take one item in the list and use it to replace to XXXX in Route_XXXX_travel_time.csv on the first line. Delete it from the list.
7. replace XXXXXXXX with the required SSID name in cell 4 (and also rename the notebook from '0-Template')
8. after first run, change line in cell 12 to leeson = pd.read_csv('SSID_CSVs/SSID_XXXXXXXX.csv') where XXXXXXXX is the actual SSID number; this allows the notebook to be loaded from this point (after necessary imports)
9. Observations on anything interesting you notice would be good.
