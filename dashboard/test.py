# -*- coding: utf-8 -*-
"""
Created on Sun May  6 17:17:35 2018

@author: yashr
"""

import pandas as pd
import numpy as np

df = pd.read_csv("../plots/lib/messages.csv", names=['Roles', 'Timestamp', 'Channel', 'Content', "User ID", "Toxicity"], parse_dates=[1])

df['Regular'] = df['Roles'].str.contains("Regular")
df['Mapachito'] = df['Roles'].str.contains('Mapachito')
df['Timestamp'] = df['Timestamp'].dt.tz_localize('UTC').dt.tz_convert("America/Los_Angeles")

df['Month'] = df['Timestamp'].dt.month
df['Day'] = df['Timestamp'].dt.day
df['Hour'] = df['Timestamp'].dt.hour

reg_table = df.groupby("User ID").agg({
        'Month': pd.Series.nunique, 
        "Content": pd.Series.count,
        "Regular": any, 
        "Mapachito": any
        })
reg_table['Count'] = reg_table['Content']/reg_table['Month']

#AddThreshold = reg_table[reg_table['Regular']]['Count'].mean()
AddThreshold = reg_table['Count'].mean()

#RemoveThreshold = reg_table['Count'].mean()
RemoveThreshold = reg_table[reg_table['Regular'] == False]['Count'].mean()

add_list = reg_table[(reg_table['Regular'] == False) & (reg_table['Count'] > AddThreshold)]
kill_list = reg_table[reg_table['Regular'] & (reg_table['Count'] < RemoveThreshold)]

#day = pd.Timedelta("1 days")
last_timestamp = df.iloc[len(df)-1]['Timestamp']

#inrange = df[df['Timestamp'].between(last_timestamp-day, last_timestamp)]
pastday = df[df['Timestamp'].between(last_timestamp.floor('D'), last_timestamp)]

#table = inrange.groupby("Hour").count()
#table = inrange.groupby([(inrange['Timestamp'].dt.day),(inrange['Timestamp'].dt.hour)]).count()

counts = pastday.groupby(pastday['Timestamp'].dt.hour)['Timestamp'].count()


x = counts.index
y = counts






#------------------------------------------------------------------------------
#Toxicity Shit

#find how toxic an average day is
#find how toxic the last day is
#see how much more toxic it is (%increase?)
avg_day = df.groupby(df['Timestamp'].dt.day)['Toxicity'].mean().mean()
past_day_toxicity = pastday['Toxicity'].mean()
percent_increase = (past_day_toxicity-avg_day)/avg_day


np.set_printoptions(suppress=True)
toxicity = df.groupby('User ID')['Toxicity'].mean()
toxicity[toxicity.index == 225119587392421888]

#identify toxic users

#identify toxic channels?
#find if a channel is being more toxic than the norm