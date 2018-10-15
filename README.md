# Team-10 Dublin Bus group research project

This is a copy of the repository for the group research project I collaborated on with three other students as a part of my MSc in Computer Science at UCD.

As data science lead, most of my contributions were in the cleaning and analysis of the data, feature engineering, and creation of predictive models.

Below, I will first give a brief overview of the project and then outline my own major contributions.  For more detail, please refer to my personal project report ([UCD_CS_47360_Report_IF.pdf](../master/DublinBus_Project_Report.pdf)).

### Project Outline

This project involved analysing historic [Dublin Bus GPS data](https://data.smartdublin.ie/dataset/dublin-bus-gps-sample-data-from-dublin-city-council-insight-project "Updated link to Dublin Bus data") and [Met Eireann weather data](http://archive.met.ie/climate-request/ "Updated link to Met Eireann data") in order to create dynamic travel time estimates.  The data covered 56 full days - most of November 2012 and all of January 2013.  The aim was to develop a mobile-optimised web app, which when presented with any bus route, an origin stop and a destination stop, a time, a day of the week, and current weather, would produce and display via the interface an estimate of travel time for the selected journey.

The team took the approach of modelling the bus data by treating road segments between consecutive stops as the basic units of routes, and producing models to predict the time taken to traverse each of these units.  These models were based on the travel time data accumulated from all buses traversing the segment.  The hope was that the additional traffic information garnered by this approach would provide greater accuracy than focusing on individual bus routes in isolation.

### Personal contributions

From the [DataCleaningPrep](../master/project/DataCleaningPrep) folder:
  * [Exploring_siri20121106](../master/project/DataCleaningPrep/0_Exploring_siri20121106.ipynb) Preliminary analysis of the first full day’s worth of data provided from the entire ﬂeet of operational Dublin Bus vehicles.
  * [Initial_Cleaning_of_All_via_Pickle](../master/project/DataCleaningPrep/1_Initial_Cleaning_of_All_via_Pickle-v3.ipynb) Initial cleaning of full raw data.
  * I collaborated with my team-mate Wen-Ting Chang on most of the rest of the contents of this folder, but the bulk of the coding was done by her.
  
All the notebooks in the [SSID_Analysis](../master/project/SSID_Analysis), [Modelling](../master/project/Modelling) and [Final_Model_Production+Results](../master/project/Final_Model_Production+Results) folders are my work, with the exception of the get_stops_sequence_by_googletransit and SSID_XXXX_travel_time_csvs_creation files, which I worked with Wen-Ting Chang on.

I also produced all the documentation for these folders.

*Note that some of these notebooks need to be downloaded for viewing due to size or GitHub display-formatting issues.
