import pandas as pd
import numpy as np
import os
from datetime import datetime

#change python current working directory
print(os.getcwd())
#change python current working directory
os.chdir('/Users/ucast/Desktop/PScript')
print(os.getcwd())

#csv file variable
data_url = 'devices_20210222_1127.csv'
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

#import vehicle master list
#df_v = pd.read_csv("SMRT-master.csv", index_col = 'vehicle_id')

#import test plate list
df_v = pd.read_csv("23testplate.csv", index_col = 'vehicle_id')

df_smrt = pd.merge(df,
                     df_v,
                     on ='vehicle_id',
                     how ='right')
#print(df_smrt)
#hired & on v28
v28h = df_smrt[(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1028.201216_RC', na=False))
        & (df_smrt['Hired Status'] == 'Hired')]

print('hiredOn28 '  + str(len(v28h)))


#hired & not on v28
nv28h = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1028.201216_RC', na=False))
        & (df_smrt['Hired Status'] == 'Hired')]
print('nv28h qty: ' + str(len(nv28h)))

#hired & not on v28 & on OTA v15
nv28h15 = df_smrt[(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1028.201216_RC', na=False))
        & (df_smrt['Hired Status'] == 'Hired')]
print('nv28hOTA15 qty: ' + str(len(nv28h15)))

#hired & not on v28 and has 2 ota client
nv28h2ota = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1028.201216_RC', na=False))
        & (df_smrt['Hired Status'] == 'Hired')
        & (df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.15', na=False))
        & (df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1', na=False))
       ]
print('nv28h2ota qty: ' + str(len(nv28h2ota)))

#hired & not on v28 and ota client v11
nv28h11 = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1028.201216_RC', na=False))
        & (df_smrt['Hired Status'] == 'Hired')
        & ~(df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.15', na=False))
        & (df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1.0.11', na=False))
       ]
print('nv28h11 qty:' + str(len(nv28h11)))

#hired & not on v28 and ota client v8
nv28h8 = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1028.201216_RC', na=False))
        & (df_smrt['Hired Status'] == 'Hired')
        & ~(df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.15', na=False))
        & (df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1.0.8', na=False))
       ]
print('nv28h8 qty: ' + str(len(nv28h8)))

#hired & not on v28 and ota client v7
nv28h7 = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1028.201216_RC', na=False))
        & (df_smrt['Hired Status'] == 'Hired')
        & ~(df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.15', na=False))
        & (df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1.0.7', na=False))
       ]
print('nv28h7 qty: ' + str(len(nv28h7)))

#hired & on v28
v27h = df_smrt[(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1027', na=False))
        & (df_smrt['Hired Status'] == 'Hired')]

#print(v27h)

#for export CSV to have timestamp
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d%b%Y %H%M%S")
print(timestampStr)

df_smrt.to_csv(str(timestampStr)+'.csv', index=False)
