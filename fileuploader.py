import pandas as pd
import numpy as np
import os
from datetime import datetime

#change python current working directory
print(os.getcwd())
#change python current working directory
os.chdir('/Users/ucast/Desktop/PScript')
print(os.getcwd())
#############################clean data####################
#csv file variable
data_url = 'devices_20210420_0920.csv'
df = pd.read_csv(data_url, usecols = ['mdt_id','vehicle_id', 'list_of_app', 'rpt_time'])

#Manually filter last report by latest date and remove the duplicated entries that has an older date
df['rpt_time'] =pd.to_datetime(df.rpt_time,  dayfirst=True)
df.sort_values('rpt_time', ascending = False , inplace = True)

#trim vehicle plate whitespace
df['vehicle_id'] = df.vehicle_id.str.replace(' ', '')

df.set_index('vehicle_id')

#drop duplicated plate number
df.drop_duplicates(subset ="vehicle_id",
                     keep = "first", inplace = True)

#############################filter base on selected list####################
#import vehicle master list
df_v = pd.read_csv("/Users/ucast/Desktop/LiveOTA/batch4.csv", index_col = 'vehicle_id')
#ongoing = pd.read_csv("/Users/ucast/Desktop/LiveOTA/ongoing.csv", squeeze = True)
print(df_v)

#print(ongoing)
df_smrt = pd.merge(df,
                     df_v,
                     on ='vehicle_id',
                     how ='right')
print(df_smrt)
df_not34 = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1034', na=False))]

#df_not34 = df_smrt[(~df_smrt['vehicle_id'].isin(ongoing)) & ~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1034', na=False))]


#print(df_not34)
#not34 = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1034', na=False))]

#fileuploaderv9 = df_smrt[(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1034', na=False))]
#for export CSV to have timestamp
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d%b%Y %H%M%S")
print(timestampStr)

print(df_not34)



df_smrt.to_csv(str(timestampStr)+'.csv', index=False)
