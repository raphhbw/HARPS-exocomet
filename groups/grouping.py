'''
Updated 24-01-2023

Form groups for every individual targets
'''
import pandas as pd
import numpy as np
from statistics import mode

# Load metadata + spectra
metadata = pd.read_pickle('../build-dataset/res/meta/metadata.pkl')
# sK = np.load('../build-dataset/res-21-03-22/spec/sK.npy')
# sH = np.load('../build-dataset/res-21-03-22/spec/sH.npy')
# fits_list = np.load('../build-dataset/res-21-03-22/fits_list-21-03.npy')
print('metadata + spectra loaded')

### Get Groups acoording to reduced name + coordinates ###
# Group metadata by reduced name (grouby object)
r = metadata.groupby(['Reduced'], as_index=False)

# Assign group number to the groubpy reduced name (DataFrame object)
metadata['Nb Obs'] = np.zeros(len(metadata))
agg_func_count = {'Alpha': 'median', 'Delta': 'median', 'Nb Obs':'count'}
reduced = r.agg(agg_func_count)

reduced.insert(0, 'Groups', np.arange(len(reduced)))

# Group the reduced name by coordinates -ie. Alpha, Delta (groupby object)
redu_coords = reduced.groupby(by=[reduced.Alpha,reduced.Delta], as_index=False)

# Updating group numbers according to groupby coordinates (DataFrame object)
groups = redu_coords['Groups'].apply(lambda g: g.values[0] if (len(g)>1) else g.values[0])
groups = groups.rename(columns={'Groups': 'New Groups'})

### Map back the group number to metadata ###
group_redu = reduced.join(groups.set_index(['Alpha', 'Delta']), on=['Alpha', 'Delta'])

meta = metadata.copy() # keep metadata authentic
full = meta.join(group_redu.set_index('Reduced')['New Groups'], on= 'Reduced')
full = full.drop(columns=['Nb Obs'])

# Get all information for all the different groups
full_grouped = full.groupby('New Groups')

all_groups = full_grouped.first() # df to be updated with new data
all_groups['Sanitised'] = full_grouped['Sanitised'].apply(lambda san: mode(san))
all_groups['Reduced'] = full_grouped['Reduced'].apply(lambda red: mode(red))
all_groups['Object'] = full_grouped['Object'].apply(lambda obj: mode(obj))
all_groups['Alpha'] = full_grouped['Alpha'].apply(lambda alph: mode(alph))
all_groups['Delta'] = full_grouped['Delta'].apply(lambda delt: mode(delt))


all_groups = all_groups.drop(columns=['SNR','Date', 'RV', 'Checked', 'Coordtype',	'Epoch',	'Epochsystem',	'Equinox',	'Parallax',	'PM Alpha',	'PM Delta',	'Airmass',	'RA',	'Dec' ])
all_groups = all_groups.reset_index(drop =False)

print(full)
print(all_groups)
full.to_pickle('../build-dataset/res/meta/full_metadata.pkl')
all_groups.to_pickle('../build-dataset/res/meta/groups.pkl')