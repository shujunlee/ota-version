import os
import pandas as pd
import numpy as np

#change python current working directory
print(os.getcwd())

#change python current working directory
os.chdir('/Users/ucast/Desktop/PScript')
print(os.getcwd())

#import filename
data_url = 'devices_20210222_1127.csv'
df = pd.read_csv(data_url, usecols = ['mdt_id','vehicle_id', 'list_of_app', 'rpt_time'])

#Manually filter last report by latest date
df['rpt_time'] = pd.to_datetime(df.rpt_time)
df.sort_values('rpt_time', ascending = False , inplace = True)

#trim vehicle plate whitespace
df['vehicle_id'] = df.vehicle_id.str.replace(' ', '')

#set index to 'vehicle_id'
df.set_index('vehicle_id')

#drop duplicated plate number
df.drop_duplicates(subset ="vehicle_id",
                     keep = "first", inplace = True)

#print(df.loc[df['vehicle_id'] == "SHC4480K"])

#import vehicle master list in new df
df_v = pd.read_csv("SMRT-master.csv", index_col = 'vehicle_id')

#merge the 2 df
df_smrt = pd.merge(df,
                     df_v,
                     on ='vehicle_id',
                     how ='right')

df_smrt['list_of_app'][0].split(',')
