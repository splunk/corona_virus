import os
import glob
import pandas as pd

#set working directory
splunk_home = os.environ['SPLUNK_HOME']
extension = "csv"
os.chdir(splunk_home+"/etc/apps/corona_virus/git/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports")

all_filenames = [i for i in glob.glob('*20.{}'.format(extension))]
dfs = (pd.read_csv(fname) for fname in all_filenames)

combined_csv = pd.DataFrame()

frames = []
#Use counter for keeping track of which filename being operated on
counter = 0
for df in dfs:
        column_check = 0
        dfObj = pd.DataFrame()
        dfObj["Latitude"] = []
        dfObj["Longitude"] = []
        dfObj["Country"] = []
        dfObj["State"] = []
        dfObj["Deaths"] = []
        dfObj["Confirmed"] = []
        dfObj["Recovered"] = []
        dfObj["County"] = []
        dfObj["FIPS"] = []
        for c in df.columns:
            if all_filenames[counter]=="03-24-2020.csv":
                print(dfObj)
            if c.lower().startswith('country'):
                dfObj["Country"] = df[c].rename(columns={c:"Country"})
                continue
            if 'state' in c.lower():
                dfObj["State"] = df[c].rename(columns={c:"State"})
                continue
            if 'confirmed' in c.lower():
                dfObj["Confirmed"] = df[c].rename(columns={c:"Confirmed"})
                continue
            if 'deaths' in c.lower():
                dfObj["Deaths"] = df[c].rename(columns={c:"Deaths"})
                continue
            if 'recovered' in c.lower():
                dfObj["Recovered"] = df[c].rename(columns={c:"Recovered"})
                continue
            if c=='Latitude' or c=="Lat":
                dfObj["Latitude"] = df[c].rename(columns={c:"Latitude"})
                continue
            if c=="FIPS":
                dfObj["FIPS"] = df[c].rename(columns={c:"FIPS"}).astype('category')
                continue
            if c=="Admin2":
                dfObj["County"] = df[c].rename(columns={c:"Admin2"})
                continue
            if c=="Long" or c=="Long_":
                dfObj["Longitude"] = df[c].rename(columns={c:"Longitude"})
                continue
        dfObj["_time"] = all_filenames[counter].replace(".csv","")
        dfObj["file_name"] = all_filenames[counter]
        frames.append(dfObj)
        counter = counter + 1
combined_csv = pd.concat(frames,copy=False,axis=0,ignore_index=True)
#save to csv
combined_csv.to_csv( splunk_home+"/etc/apps/corona_virus/lookups/combined_jhu.csv", index=False, encoding='utf-8-sig')
