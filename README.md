# About

Adapted code from https://github.com/petergardfjall/garminexport

Barebones Python code to **download Body Score from Garmin**. Assumes you have an account with Garmin Connect. 

Executing this will ask you to enter your Garmin username/email and password. However, these are not stored after execution and acts like any browser (e.g. Chrome) using Garmin Connect.<br/>

This does not work when Garmin turns on captchas. This will happen if you ping their server too many times. Resets after awhile (maybe 24 hours?). <br/>
Instead look at garth for solutions. <br/>
You can also manually copy and paste data using F12 when signed into Garmin Connect. <br/>



![fig](https://github.com/physioforecast/garminexport/assets/6562289/5a62dbe3-4d22-445b-a444-f9164ea93f3a)




# Installation

Make sure Python is installed and requirements (see file).

Then download zipped code (or clone), and run grab_bodyscore.py . 

![Untitled presentation](https://github.com/physioforecast/garminexport/assets/6562289/202bb9e1-830f-43c7-a55a-2626d46b8296)

# Execution

python grab_bodyscore.py \<Garmin username\> \<Garmin password\> \<start-date YYYY-MM-DD\> \<end-date YYYY-MM-DD\> \<Folder path for downloads\>

