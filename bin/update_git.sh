#!/bin/sh
# Update the sub repos to the current head of the repo.  This isn't
# necessary, but it stops a bunch of confusing messages going into
# main the first time the submodules are updated from the remote
cd $SPLUNK_HOME/etc/apps/corona_virus/git/COVID-19/
git checkout master
cd $SPLUNK_HOME/etc/apps/corona_virus/git/NYState-COVID-19-Tracker/
git checkout master

# Here is where we actually upll updates from the submodule data sources.
cd $SPLUNK_HOME/etc/apps/corona_virus
git submodule foreach git pull origin master
