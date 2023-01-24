'''
Updated 24-01-2023

Create Groups for every individual targets
'''
import pandas as pd
import numpy as np

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

# print(np.array_equal(full.Object.to_numpy(), metadata.Object.to_numpy()))
# print(full)
full.to_pickle('../build-dataset/res/meta/full_metadata.pkl')
group_redu.to_pickle('../build-dataset/res/meta/groups.pkl')