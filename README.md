# Coronavirus App

This is a set of dashboards for analyzing the Corona Virus using Splunk. 

Contributors to this app: Ryan O'Connor, Miranda Luna, Caleb Dyck, Anthony Barbato, Giovanni Mola

<em>The Splunk Corona Virus dashboard provided in this GitHub repo is an informational tool provided by Splunk without charge to all those who are working to understand and combat COVID-19.  The dashboard is intended for informational purposes only and relies entirely on data provided by various third-parties including, inter alia, Johns Hopkins University and any information entered by the user. [https://github.com/CSSEGISandData/COVID-19](https://github.com/CSSEGISandData/COVID-19). This dashboard is not for commercial use and is intended and should be used to provide background and context on the evolving COVID-19 situation.  Splunk disclaims any and all representations and warranties with respect to the dashboard, including accuracy, fitness for use and merchantability.</em>

## Installing the App

This app should be installed directly into $SPLUNK_HOME/etc/apps. You simply clone the app directly into that directory and it will be self-contained. Please see the install instructions below. 

**You must use the git clone method for this app to work properly. See [Cloning this App](#cloning-this-app)**

### App Requirements

* This app currently is supported on Linux only. 

* For the Confirmed Cases/Locations Overlay dashboard to load optimally, please ensure you have the [Maps+ App installed from Splunkbase](https://splunkbase.splunk.com/app/3124/). 

* Please also ensure you are installing using the git clone method below. 

### Cloning this App

This package depends on a submodule from here: https://github.com/CSSEGISandData/COVID-19 which is the main source of data for the Coronavirus. As a result, when you run git [clone](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository), please add the --recurse-submodules parameter after the clone. So for example:

`git clone --recurse-submodules https://github.com/splunk/corona_virus.git`

This will ensure the required submodule is cloned into the correct directory inside of the app. Once you have cloned the app, please restart Splunk. 

## Dashboard Information

1. Coronavirus 
    ![image](https://user-images.githubusercontent.com/11879871/77706120-dd31e180-6f97-11ea-96e0-89d1a2182896.png)
    1. This is a static analysis of the Coronavirus. 
1. covid-19 Patterns & Trends
    ![image](https://user-images.githubusercontent.com/11879871/77706906-08b5cb80-6f9a-11ea-9b3b-0517f99389bb.png)
    1. This is the same dashboard as the one publicly available on https://covid-19.splunkforgood.com 
1. Coronavirus - Timelapse
    1. This is a timelapse of the Coronavirus from the first day it was detected, until the current day. 
1. Confirmed Cases/Locations Overlay
    ![image](https://user-images.githubusercontent.com/11879871/77705786-eff7e680-6f96-11ea-945e-29ed55261ecc.png)
    1. This is a dashboard that can be used to overlay locations of your choosing, with confirmed cases of COVID-19. By default, we are simply using U.S. State Capitals as an example. But you can choose to modify locations.csv to fit your own purposes. 
    
## Lookup Table Updating

### confirmed.csv, recovered.csv, and deaths.csv

There is a scripted input inside of this app that is **enabled by default**. It can be found in the GUI by going to Settings > Data Inputs > Scripts and enabling the input "update_git.sh". This script will be used to pull the latest csse timeseries data from JHU and create a symbolic link to each file in the $SPLUNK_HOME/etc/apps/corona_virus/lookups directory. 

This scripted input will send it's output by default to `index=main sourcetype=git_update_corona`. You can use this index/sourcetype to find out when the latest update to the Coronavirus git repository took place. 

A search to find out when the last time the JHU Git Repository was updated would look like the following:

```
index=main sourcetype=git_update_corona _raw!="*Already up to date.*" 
| head 1 
| eval time=strftime(_time,"%m/%d/%Y %H:%M:%S") 
| table time
```

An example update would look like this:

```
2020-03-09 20:59:32	Entering 'git/COVID-19'

Updating 382bda4..473681f
Fast-forward
 .../time_series_19-covid-Confirmed.csv             | 541 ++++++++++-----------
 .../time_series_19-covid-Deaths.csv                | 541 ++++++++++-----------
 .../time_series_19-covid-Recovered.csv             | 541 ++++++++++-----------
 3 files changed, 801 insertions(+), 822 deletions(-)
 ```
 
### combined_jhu_us_daily.csv

This file contains US State Level Data including Hospitalizations and Tests. It is a combination of all previous CSSE US Daily Reports. I also have added the script I use to generate this titled merge_us.py. 

### combined_jhu.csv

This file contains US State Level Data, County Level Data, and is a combination of all previous CSSE Daily Reports. 

I've added a script that I use to merge all of the daily reports into one massive csv file. This can be used to get historical State Level time series data once again. I will keep this file up to date as often as JHU provides daily reports. It is a lookup table called combined_jhu.csv. If you'd like to update it on your own or explore the methodology I use to merge, I am providing more details below. 

#### Background of this file
As mentioned in the documentation:

"This package depends on a submodule from here: https://github.com/CSSEGISandData/COVID-19 which is the main source of data for the Coronavirus."

#### Methodology for creating combined_jhu.csv

Our merge.py file simply takes the daily reports provided from the aforementioned Github repository (specifically the CSSE Daily Reports), and appends all of them onto one another. The only adjustment going on, is standardizing on field names. For example: in some files we have "Province/State" and in others we have "Province/State". This adjustment of field names allows us to search commonly for "Country" Across all dates as far back as JHU provides daily reports. I also add a column called "file_name" so you can determine which file the record came from. 

This methodology creates a massive CSV with all of the following fields:

-         "Latitude"
-         "Longitude"
-         "Country"
-         "State"
-         "Deaths"
-         "Confirmed"
-         "Recovered"
-         "County"
-         "FIPS"
-         "file_name"

_Note: Not all of these fields are filled out for all daily reports. For example, County level data only started coming in very recently. Those fields will be blank for some files._ 

### To Update combined_jhu.csv on your own

This script does require pandas, which does not ship with Splunk today. But you can run the script via cron on a Linux machine to keep the file up to date. Please note that the daily reports only come in once per day, and I will be updating this file once per day. **so you don't need to do this part**. But for the sake of being open about our process, I've provided the information below. 

```
* * * * * SPLUNK_HOME="/opt/splunk" /usr/bin/python /opt/splunk/etc/apps/corona_virus/bin/merge.py
```
## Change Record

### 04/04/20
* Updated combined_jhu.csv
* Resolved issue with table on main app. Ended up cutting over to using my combined_jhu.csv which is a much easier format to work with. 
* resolved issue #16

### 04/03/20
* Updated combined_jhu.csv

### 04/02/20
* Updated combined_jhu.csv

### 04/01/20
* Updated combined_jhu.csv

### 3/30/20
* Updated combined_jhu.csv with the latest daily reports. 

### 3/29/20
* Updated combined_jhu.csv with the latest daily reports. 
* Formatted some of the main dashboard panels to work in the timelapse dashboard. Some of them include a bubble chart and also an updated table. 
### 3/28/20
* Updated combined_jhu.csv with the latest daily reports. 

### 3/27/20
* Updated combined_jhu.csv with the latest daily reports. 
* Fixed the map overlay dashboard with some fancy new colors. SPL help courtesy of Scott Haskell. 
* Updated README to provide more information. 
* Modified main dashboard to use ISO8601 Timestamps in all timeseries charts
### 3/26/20
* Added a python script called "merge.py" which you can use to merge all of the Daily reports into one massive csv file. This allows for US State level Data once again. 
* Going to be keeping a lookup table called combined_jhu.csv up to date for people to use. This will be a combination of whatever daily csse reports that are posted publicly.
* Tried to correct some of the renames of the files that JHU made this week so the symbolic links should be up to date.
* Updated Dashboards Beta to contain annotations on Area Chart
### 3/24/20
* Added a scripted input to take the latest daily report from JHU and symlink it to a lookup table called update_daily.csv
### 3/23/20
* Updated app to conform to changes in the JHU Data Repository. See the [following link](https://github.com/CSSEGISandData/COVID-19/issues/1250) for more information
* Major callout in this update is the removal of Recovered data with the hopes of more granular county level insights coming soon. 
### 3/19/20
* Merged in the public Splunk Dashboards Beta into the app. So people downloading this app can look at both Simple XML Dashboards, as well as the new dashboards beta dashboard.
* Fixed a couple bugs to make the main Simple XML Dashboard Mobile Friendly
* Turned the scripted input on by default to make setup easier for everyome
