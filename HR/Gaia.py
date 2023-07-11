from gaia_ids import Gaia_info
from gaia_query import Gaia_Search
import pandas as pd
import numpy as np

# Load list of targets
groups = pd.read_pickle('../build-dataset/res/meta/groups.pkl')
targets = groups.Sanitised.to_numpy()

# Get Gaia IDs for all targets
print('Getting Gaia IDs for targets....')
Gaia = Gaia_info()
gaia_ids = Gaia.get_gaia_info(targets)
print(gaia_ids)

# Add Gaia info to groups DataFrame
groups_w_gaia = groups.copy()
groups_w_gaia = groups.join(gaia_ids.Simbad_ID)
groups_w_gaia = groups.join(gaia_ids.Gaia_ID)
groups_w_gaia.to_pickle('../build-dataset/res/meta/groups_w_gaia.pkl')

# Get all Gaia information
print('Getting Gaia info for targets....')
Query = Gaia_Search(gaia_ids)
Query.query_gaia(r = 0.01) # search radius is 0.01 degrees
print(Query.gaia_info)