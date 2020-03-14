# Coronavirus App

This is a set of dashboards for analyzing the Corona Virus using Splunk. Created by Ryan O'Connor. 

## Installing the App

This app should be installed directly into $SPLUNK_HOME/etc/apps. You simply clone the app directly into that directory and it will be self-contained. 

### Specific Requirements for Cloning the Directory.

This package depends on a submodule from here: https://github.com/CSSEGISandData/COVID-19 which is the main source of data for the Coronavirus. As a result, when you run git clone, please add the --recurse-submodules parameter after the clone. So for example:

`git clone --recurse-submodules https://github.com/splunk/corona_virus.git`

This will ensure the required submodule is cloned into the correct directory inside of the app. 

## Dashboard Information

There are two dashboards here:

1. Coronavirus 
    1. This is a static analysis of the Coronavirus. 
1. Coronavirus - Timelapse
    1. This is a timelapse of the Coronavirus from the first day it was detected, until the current day. 
1. Confirmed Cases/Locations Overlay
    1. This is a dashboard that can be used to overlay locations of your choosing, with confirmed cases of COVID-19. By default, we are simply using U.S. State Capitals as an example. But you can choose to modify locations.csv to fit your own purposes. 
    
## Lookup Table Updating

There is a scripted input inside of this app that can be enabled. It can be found in the GUI by going to Settings > Data Inputs > Scripts and enabling the input "update_git.sh". 

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
