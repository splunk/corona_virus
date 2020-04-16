cd $SPLUNK_HOME/etc/apps/corona_virus/lookups/
ln -f -s ../git/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/`ls -v ../git/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/ | grep -v README | tail -n 1` latest_daily.csv
