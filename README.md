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
    
## Lookup Table Updating

There is a scripted input inside of this app that can be enabled. It can be found in the GUI by going to Settings > Data Inputs > Scripts and enabling the input "update_git.sh". 
