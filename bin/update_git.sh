#!/bin/sh
cd $SPLUNK_HOME/etc/apps/corona_virus/git/COVID-19/
git checkout master 2>&1
cd $SPLUNK_HOME/etc/apps/corona_virus
git submodule foreach git pull origin master 2>&1
