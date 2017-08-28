Copied from the Wiki

### NOTE: Before running these files, copy them to a different folder on your home machine along with any relevant data (csv, pickle, feather) files.  Do _not_ move new data files into the GitHub folder!

Files to be run in the following order:

_1. Initial_Cleaning_of_All_via_Pickle-v3.ipynb_

* Inputs the 4 Pickle files containing full dataset, as provided by Wen Ting.
* Carries out initial cleaning.
* Outputs single full dataset feather file to be loaded into second notebook.
* All fields starting with '#0' are purely descriptive and can be skipped to speed up processing (easiest way to ensure this if running whole notebook is to turn all such cells from Code to Markdown first).

_2. Stage_Two_Cleaning_v6.ipynb_

* Inputs full dataset feather file produced by first notebook.
* Also inputs stops.txt taken from googletransit20121129-1547 zip file and all three weather data files (all in: https://github.com/wjdelaney/Team-10/blob/master/project/DataAnalytics/supplemental_data_files); put these into the same folder as the notebook.
* Outputs a new full dataset feather file, further cleaned and prepared.

_3. Create_input_files_for_modelling.py_

* **Edit list of required route files before running.**
* Inputs full dataset feather file produced by second notebook.
* Outputs a feather file per route listed for input into (5) Output_SSID_Traveling_Time.py.
* Best to run in the shell

_4. Create_StopID_Lon_Lat.ipynb_

* Inputs feather file produced by second notebook.
* Inputs stops.csv taken from googletransit20121129-1547 zip file (get here: https://github.com/wjdelaney/Team-10/blob/master/project/DataAnalytics/supplemental_data_files/googletransitdbfeedp20121129-1547.zip)
* Outputs input1_StopID_LonLat.csv file for input into (5) Output_SSID_Traveling_Time.py.

_5. Output_SSID_Traveling_Time.py_

* **Edit list of required route files (list name = `route_list`, at end of script, same as in step three) before running.**
* Inputs feather route files produced in step three for processing.
* Inputs input1_StopID_LonLat.csv, as produced in fourth step.
* Outputs a feather file per route listed (Route_XXXX_after.feather), plus a csv file with target feature of each route calculated (Route_XXXX_travel_time.csv), the latter for input into the SSID_Analysis stage.  Exported to /input2_routes/
* Best to run in the shell
* Needs optimisation


_supplemental_data_files:_

This folder contains the weather data being used from three Dublin weather stations, and the NTA GTFS Dublin Bus data from 2012, in googletransitdbfeedp20121129-1547.zip
