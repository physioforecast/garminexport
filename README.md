# About

Adapted code from https://github.com/petergardfjall/garminexport

Barebones Python code to download Body Score from Garmin. Assumes you have an account with Garmin Connect. 

Executing this will ask for you to enter your Garmin username/email and password. However, it is not stored after the session and acts like an browser (e.g. Chrome) using Garmin Connect. 

![fig](https://github.com/physioforecast/garminexport/assets/6562289/83ff43ff-abe4-4c60-b0b9-115b92a04bc2)



# Installation

Make sure Python is installed and requirements (see file).

Then either git clone repo or download zip, and run grab_bodyscore.py

# Execution

python grab_bodyscore.py \<Garmin username\> \<Garmin password\> \<start-date YYYY-MM-DD\> \<end-date YYYY-MM-DD\> \<Folder path for downloads\>

