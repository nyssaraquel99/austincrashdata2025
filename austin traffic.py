# -*- coding: utf-8 -*-
"""
Created on Mon Nov 10 18:10:30 2025

@author: nyssa
"""

#%% import libraries
import pandas as pd
import os

#%% load data
path=os.path.dirname(__file__)
filename="Austin_Crash_Report_Data_-_Crash_Level_Records.csv"
df=pd.read_csv(f"{path}\\{filename}")

#%% format time data
format_dt="%m/%d/%Y %I:%M:%S %p"
df["datetime"]=pd.to_datetime(df["Crash timestamp"],
                             utc=True,
                             format=format_dt,
                             errors="coerce")

#%% extract year and month
df["month"]=df["datetime"].dt.month
df["year"]=df["datetime"].dt.year
df["year-month"]=(df["year"].astype("string"))+"-"+df["month"].astype("string") #YYYY-M


#%% make smaller dataframe with last five years data
df_5years=df[df["year"]>=2020]

#%% separate into counts, injuries, deaths
"""
create data subset to generate monthly crash chart
"""
# get total number of crashes per month each year
counts_5years=df_5years.groupby("year-month")[["Crash ID"]].count()
# fill out dataframe
counts_5years=counts_5years.rename(columns={"Crash ID":"Total"})
counts_5years["Deaths"]=df_5years.groupby("year-month")["death_cnt"].sum()
counts_5years["Injuries"]=df_5years.groupby("year-month")["sus_serious_injry_cnt"].sum()
# reset index and add month, year columns
counts_5years=counts_5years.reset_index()
counts_5years[["year","month"]]=counts_5years["year-month"].str.split(pat="-",expand=True)

#%% export counts as csv
counts_5years.to_csv(f"{path}\\5yearcounts2.csv",index=False)

#%% print column names
print(list(df.columns))

#%% seperate counts by travel mode
"""
create data subset to generate stacked travel mode chart
"""
# summing years 2021-2025
df21_25=df[df["year"]>=2021]
travel_counts=df21_25.groupby("year")[["Crash ID"]].count()

travel_counts=travel_counts.rename(columns={"Crash ID":"Total"})
# death nos.
travel_counts["Motorist Deaths"]=df21_25.groupby("year")["motor_vehicle_death_count"].sum()
travel_counts["Pedestrian Deaths"]=df21_25.groupby("year")["pedestrian_death_count"].sum()
travel_counts["Motorcyclist Deaths"]=df21_25.groupby("year")["motorcycle_death_count"].sum()
travel_counts["Bicyclist Deaths"]=df21_25.groupby("year")["bicycle_death_count"].sum()
travel_counts["E-Scooter Deaths"]=df21_25.groupby("year")["micromobility_death_count"].sum()
travel_counts["Other Deaths"]=df21_25.groupby("year")["other_death_count"].sum()
travel_counts["Total Deaths"]=df21_25.groupby("year")["death_cnt"].sum()
# serious injury nos.
travel_counts["Motorist Injuries"]=df21_25.groupby("year")["motor_vehicle_serious_injury_count"].sum()
travel_counts["Pedestrian Injuries"]=df21_25.groupby("year")["pedestrian_serious_injury_count"].sum()
travel_counts["Motorcyclist Injuries"]=df21_25.groupby("year")["motorcycle_serious_injury_count"].sum()
travel_counts["Bicyclist Injuries"]=df21_25.groupby("year")["bicycle_serious_injury_count"].sum()
travel_counts["E-Scooter Injuries"]=df21_25.groupby("year")["micromobility_serious_injury_count"].sum()
travel_counts["Other Injuries"]=df21_25.groupby("year")["other_serious_injury_count"].sum()
travel_counts["Total Injuries"]=df21_25.groupby("year")["sus_serious_injry_cnt"].sum()
# reset index
travel_counts=travel_counts.reset_index()

#%% export travel counts as csv
travel_counts.to_csv(f"{path}\\travelmodecounts.csv",index=False)