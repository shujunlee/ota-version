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
data_url = 'devices_20210421_0000.csv'
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
df_v = pd.read_csv("SMRT-master.csv", index_col = 'vehicle_id')

#import test plate list
#df_v = pd.read_csv("25testplate-final.csv", index_col = 'vehicle_id')

df_smrt = pd.merge(df,
                     df_v,
                     on ='vehicle_id',
                     how ='right')

df_not34 = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1034', na=True))]
df_v34 = df_smrt[(df_smrt['list_of_app'].str.contains('com.ucast.blackbox:1.0.1034', na=True))]

df_notOta20 = df_smrt[~(df_smrt['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.20', na=False))]

df_filtered = df_smrt

#texAPI filters regardless of dataframe
v34 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox:1.0.1034', na=False))]
v32 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox:1.0.1032', na=False))]
v28 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox:1.0.1028', na=False))]
v27 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox:1.0.1027', na=False))]
v21 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox:1.0.1021', na=False))]
v17 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox:1.0.1017', na=False))]
v14 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox:1.0.1014', na=False))]
noV = df_smrt['list_of_app'].isnull().sum()


blackboxSummary = {'v34': v34['vehicle_id'].count(),
                   'v32': v32['vehicle_id'].count(),
                   'v28': v28['vehicle_id'].count(),
                   'v27': v27['vehicle_id'].count(),
                   'v21': v21['vehicle_id'].count(),
                   'v17': v17['vehicle_id'].count(),
                   'v14': v14['vehicle_id'].count(),
                   'NA' : df_smrt['list_of_app'].isnull().sum(),
                   'Total': df_smrt['list_of_app'].notna().sum() + df_smrt['list_of_app'].isnull().sum()
}
Summary = pd.DataFrame.from_dict(blackboxSummary, orient='index', columns=['UCAST Blackbox'])
print(Summary)

#ota filters regardless of dataframe
ota20only = df_filtered[(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.20', na=False)) &
                 ~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1', na=False))]
ota16only = df_filtered[(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.16', na=False)) &
                 ~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1', na=False))]
ota15only = df_filtered[(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.15', na=False)) &
                 ~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1', na=False))]
ota2 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1', na=False)) &
                 (df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1', na=False))]
ota11only = df_filtered[~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1', na=False)) &
                 (df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1.0.11', na=False))]
ota8only = df_filtered[~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1', na=False)) &
                 (df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1.0.8', na=False))]
ota7only = df_filtered[~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1', na=False)) &
                 (df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1.0.7', na=False))]

ota1615 = df_filtered[((df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.16', na=True)) |
                      (df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.15', na=True))) &
                 ~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1', na=True))]

ota20onlyWithLT = df_filtered[(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.20', na=False)) &
                 ~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1', na=False)) &
                 (df_filtered['list_of_app'].str.contains('com.grab.tex:21.13.0-93c35a1', na=False))]

ota20onlyNOTLT = df_filtered[(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdmv2:1.0.20', na=False)) &
                 ~(df_filtered['list_of_app'].str.contains('com.ste.itsd.fms.agilmdm:1', na=False)) &
                 ~(df_filtered['list_of_app'].str.contains('com.grab.tex:21.13.0-93c35a1', na=False))]

OTAsummary={'ota20only':ota20only['vehicle_id'].count(),
         'ota16only':ota16only['vehicle_id'].count(),
         'ota15only':ota15only['vehicle_id'].count(),
         'ota2':ota2['vehicle_id'].count(),
         'ota11only':ota11only['vehicle_id'].count(),
         'ota8only':ota8only['vehicle_id'].count(),
         'ota7only':ota7only['vehicle_id'].count(),
         'NA' : df_smrt['list_of_app'].isnull().sum(),
         'Total': df_smrt['list_of_app'].notna().sum() + df_smrt['list_of_app'].isnull().sum()
        }

OTASummary = pd.DataFrame.from_dict(OTAsummary, orient='index', columns=['OTA Client'])
print(OTASummary)

TEXsummary={'OLD 20':ota20onlyNOTLT['vehicle_id'].count(),
         'NEW 21.13':ota20onlyWithLT['vehicle_id'].count(),
         'Total': df_smrt['list_of_app'].notna().sum() + df_smrt['list_of_app'].isnull().sum()
        }
TEXSummary = pd.DataFrame.from_dict(TEXsummary, orient='index', columns=['TEX'])
print(TEXSummary)
#fileuploader regardless of dataframe
fileupv9not34 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox.fileupload:1.0.1009', na=False)) &
                 ~(df_filtered['list_of_app'].str.contains('com.ucast.blackbox:1.0.1034', na=False))]
fileupv1  = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox.fileupload:1.0.1001', na=False))]

fileupv6  = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox.fileupload:1.0.1006', na=False))]
notfileupv9 = df_filtered[~(df_filtered['list_of_app'].str.contains('com.ucast.blackbox.fileupload', na=False))
                 ]
fileupv9 = df_filtered[(df_filtered['list_of_app'].str.contains('com.ucast.blackbox.fileupload:1.0.1009', na=False))
                 ]
fileuploader = {'fileupv9not34':fileupv9not34['vehicle_id'].count(),
                'fileupv1':fileupv1['vehicle_id'].count(),
                'fileupv6':fileupv6['vehicle_id'].count(),
                'notfileupv9':notfileupv9['vehicle_id'].count(),
                'fileupv9':fileupv9['vehicle_id'].count(),
                'NA' : df_smrt['list_of_app'].isnull().sum(),
                'Total':df_smrt['list_of_app'].notna().sum() + df_smrt['list_of_app'].isnull().sum()
}
fileuploaderSummary = pd.DataFrame.from_dict(fileuploader, orient='index', columns=['FileUploader'])
print(fileuploaderSummary)
print(notfileupv9)
#for export CSV to have timestamp
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d%b%Y %H%M%S")
date = dateTimeObj.strftime("%d %b %Y")
print(date)

#print(ota7only)
print(ota11only)
search = "SHB469B"
# print(df_smrt[(df_smrt['vehicle_id'].str.contains(search, na=True))])
# with pd.ExcelWriter('SMRT MCU Version ' + str(date) + '.xlsx') as writer:
#     df_smrt.to_excel(writer, sheet_name='Full',index=None,index_label=None)
#     df_v34.to_excel(writer, sheet_name='v34',index=None,index_label=None)
#     df_not34.to_excel(writer, sheet_name='not34',index=None,index_label=None)
#     df_notOta20.to_excel(writer, sheet_name='notOTA20',index=None,index_label=None)
#     Summary.to_excel(writer, sheet_name='Summary')
#     OTASummary.to_excel(writer, sheet_name='OTASummary')
#     ota20onlyWithLT.to_excel(writer, sheet_name='tex v21',index=None,index_label=None)

ota11only.to_csv(str(timestampStr)+'.csv', index=False)
