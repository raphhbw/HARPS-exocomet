'''
Updated 24-01-23
Create groups from full_metadata.pkl
Makes a folder for each group - named by most common reduced name in group
'''
import pandas as pd
import numpy as np
import os, sys, glob
from statistics import mode


# Load metadata + spectra
metadata = pd.read_pickle('../build-dataset/res/meta/full_metadata.pkl')
sK = np.load('../build-dataset/res/spec/sK.npy')
sH = np.load('../build-dataset/res/spec/sH.npy')
fits_list = np.array(sorted(glob.glob('../fits/ADP.*.fits')))
# print(fits_list)
# fits_list = np.load('../build-dataset/res/fits_list.npy')
wH = np.load('../build-dataset/res/wavelengths/wH.npy')
wK = np.load('../build-dataset/res/wavelengths/wK.npy')
rvH = np.load('../build-dataset/res/wavelengths/rvH.npy')
rvK = np.load('../build-dataset/res/wavelengths/rvK.npy')
print('metadata + spectra + wavelengths loaded')

groups = pd.unique(metadata['New Groups'])
dataset_path = '../dataset/'

for i,group in enumerate(groups):

    group_df = metadata[metadata['New Groups'] == group]
    idx = group_df.index.values
    name = mode(group_df['Reduced']) # Most common reduced name in group

    group_sK = sK[idx,:]
    group_sH = sH[idx,:]
    group_fits = fits_list[idx]

    # print(idx)
    # print(sK[idx,:].shape)
    # print(group_df.reset_index())
    # print(name)

    group_path = dataset_path + name

    if os.path.exists(group_path) == True:
        print('Name {} already given to a folder'.format(name))
        sys.exit()
    else:
        os.mkdir(group_path)
        os.mkdir(group_path + '/spec')
        os.mkdir(group_path + '/wavelength')
        os.mkdir(group_path + '/meta')

        group_df.reset_index().to_pickle(group_path + '/meta/group_df.pkl')
        np.save(group_path + '/spec/sH.npy', group_sH)
        np.save(group_path + '/spec/sK.npy', group_sK)
        np.save(group_path + '/meta/fits.npy', group_fits)
        np.save(group_path + '/wavelength/wH.npy', wH)
        np.save(group_path + '/wavelength/wK.npy', wK)
        np.save(group_path + '/wavelength/rvH.npy', rvH)
        np.save(group_path + '/wavelength/rvK.npy', rvK)

    print('{}/{}'.format(i+1, len(groups)))

