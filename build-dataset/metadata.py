import pandas as pd
# import numpy as np
from GetData import GetSpectra
import glob

input_fits_path = "../fits/"

file_list = sorted(glob.glob(input_fits_path + 'ADP.*.fits'))
# np.save('fits_list.npy', file_list)

allkeys = ['OBJECT', 'HIERARCH ESO TEL TARG ALPHA', 'HIERARCH ESO TEL TARG DELTA', 'SNR', 'DATE-OBS',
        'HIERARCH ESO TEL TARG RADVEL', 'HIERARCH ESO TEL TARG COORDTYPE', 'HIERARCH ESO TEL TARG EPOCH',
        'HIERARCH ESO TEL TARG EPOCHSYSTEM', 'HIERARCH ESO TEL TARG EQUINOX', 'HIERARCH ESO TEL TARG PARALLAX',
        'HIERARCH ESO TEL TARG PMA', 'HIERARCH ESO TEL TARG PMD', 'HIERARCH ESO TEL AIRM START', 'RA', 'DEC']

df = pd.DataFrame(data={'Object': [], 'Alpha': [],'Delta': [], 'SNR': [], 'Date': [], 'RV': [],
                        'Coordtype': [], 'Epoch': [], 'Epochsystem': [],'Equinox': [], 'Parallax': [],
                        'PM Alpha': [], 'PM Delta': [],'Airmass': [] , 'RA': [], 'Dec': [] , 'Checked':[]})

# In case error occurs during download
loaded = False
# loaded = True

if loaded is True:
# ========== Import main_df ===================================================
    df = pd.read_pickle('main_df.pkl')
    print(df)

    start = df[df['Checked'] == True].iloc[[-1]].index
# =============================================================================

MetaData = GetSpectra() 

for i, file in enumerate(file_list):

    if loaded is True:
        if i <= start:
            continue
    
    df = MetaData.get_metadata(i, file, allkeys, main_df = df)
    
    # print(Data.main_df)
    print('{}/{}'.format(i+1,len(file_list)))
    
    if i%20 == 0:
        df.to_pickle('res/meta/metadata.pkl')
        # np.save('corrupt.npy', np.array(MetaData.corrupt_fits))
        MetaData.corrupt.to_pickle('res/meta/corrupt.pkl')
        print('Saved')
        print('----------------------')

        
df.to_pickle('res/meta/metadata.pkl')
# np.save('corrupt.npy', np.array(MetaData.corrupt_fits))
MetaData.corrupt.to_pickle('res/meta/corrupt.pkl')
print('Saved')
print('----------------------')
print(df)
print(MetaData.corrupt)