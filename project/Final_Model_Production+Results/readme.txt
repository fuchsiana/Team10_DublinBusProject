Copied from the Wiki

NOTE: Before running these programs, copy them to a different folder on your home machine along with any relevant data csv files. Do not move new data files into the GitHub folder.

The "model_results_charts_and_averages" notebook and all "model_results" CSV files can be viewed here as they are.

For everything else, take the following preparatory steps:

1. Create folder named "Route_XXXX_travel_time_csvs" and ensure all Route CSVS (available in one zip at https://www.sendspace.com/file/l27g51) are contained within it.

2. Create folder named "SSID_XXXX_travel_time_csvs" and run the "SSID_XXXX_travel_time_csvs_creation" notebook to populate it with the required SSID CSV files. Ensure you only do this once

3. Export the files from "googletransitdbfeedp20121129-1547.zip" (available here: here: https://github.com/wjdelaney/Team-10/blob/master/project/DataAnalytics/supplemental_data_files/googletransitdbfeedp20121129-1547.zip) into a folder named "googletransitdbfeedp20121129-1547".

4. Ensure the folder contains the "JPID_Length.csv" file (and the "use_speed_and_distance_get_outlier_bound.csv" file, if you are running the "output_SSID_model_pkls+csvs_GBR_GeopyMethod_OutliersCut" notebook).

5. If you are running a pickle producing file, make sure you create a folder with the name specified at the top of the notebook before running it.
