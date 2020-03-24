cd $SPLUNK_HOME/etc/apps/corona_virus/lookups/
ln -f -s ../git/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/`ls -rt ../git/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/ | tail -n1` latest_daily.csv
