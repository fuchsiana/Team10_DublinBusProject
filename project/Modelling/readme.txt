Copied from the Wiki.

NOTE: Before running these files, copy them to a different folder on your home machine along with any relevant data csv files. Do not move new data files into the GitHub folder, unless you're uploading a new SSID analysis.

Before running any file, ensure you have created a folder named "Route_XXXX_travel_time_csvs" containing all Route CSVs (available in one zip at https://www.sendspace.com/file/l27g51) within it.

There are three Modelling Template notebooks:

1. "Multiple_Modelling_of_SSID_template", which runs a variety of models via Scikit-learn on the data using a 70/30 training/testing split
2. "RSCV_Modelling_of_SSID_template", which uses RansomizedSearchCV via Scikit-learn to test out a range of hyper-parameters for estimators Support Vector Machine Regression, Gradient Boosting Regression, and Random Forest Regression on a 70% training split of the data, before testing the chosen best hyper-parameters on the 30% testing split.
3. "RSCV_Modelling_of_SSID_template_v2_GBR focus", which does the same as no.2 but focusing only on Gradient Boosting Regression.

To create a new file from any of these:

1. Extract stop_times.txt and trips.txt from the zip here: https://github.com/wjdelaney/Team-10/blob/master/project/DataAnalytics/supplemental_data_files/googletransitdbfeedp20121129-1547.zip and place them in the same folder.

2. In the second cell, enter the values for the variables for the number of cores to be used and the SSID number to be modelled.

3. If you wish to create a CSV file of the data for the SSID being modelled, ensure a folder named "SSID_CSVs' has been created in the same folder as the notebook. If you do not wish to do so, please comment out the relevant cell (the final cell before the "Analysis of target feature TravelTime" section).

4. Change the hyper-parameter ranges to search for each estimator as you see fit.
