from astroquery.simbad import Simbad
import pandas as pd
import numpy as np

class Gaia_info():

    # Create personalised Simbad search
    gaia_simbad = Simbad()
    gaia_simbad.remove_votable_fields('coordinates')
    gaia_simbad.add_votable_fields('id(gaia)')
    gaia_simbad.get_votable_fields()
    gaia_simbad.TIMEOUT = 10000 # sets the timeout to 100s

    def __init__(self):
        pass

    def get_gaia_info(self, targets):
        xmatch = self.simbad_xmatch(targets)
        corrected_xmatch = self.rm_duplicates(xmatch)
        return self.join_xmatch(targets, corrected_xmatch)

    def simbad_xmatch(self, t):
        simbad_res = self.gaia_simbad.query_objects(t)
        return simbad_res.to_pandas()

    def rm_duplicates(self, dataframe):
        nb = dataframe.SCRIPT_NUMBER_ID
        counts = np.bincount(nb)

        vals = np.where(counts > 1)[0]
        # print(vals)

        for value in vals:
            idx = np.where(dataframe.SCRIPT_NUMBER_ID == value)[0]
            # print(idx)
            # The first Simbad xmatch is the real one
            dataframe = dataframe.drop(idx[1:]).reset_index(drop=True) # Keep the first Simbad xmatch
        
        return dataframe

    def join_xmatch(self, t, df):
        target_df = pd.DataFrame(data={'Target':t})
        df['SCRIPT_NUMBER_ID'] -= 1 # Correcting index
        gaia_info = target_df.join(df.set_index('SCRIPT_NUMBER_ID'))
        gaia_info.rename(columns = {'MAIN_ID':'Simbad_ID', 'ID_gaia':'Gaia_ID'}, inplace = True)
        return gaia_info
    