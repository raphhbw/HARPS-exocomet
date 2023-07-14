import pandas as pd
from astroquery.mast import Catalogs
import numpy as np

class Gaia_Search():

    def __init__(self, gaia_xmatch):
        self.gaia_xmatch = gaia_xmatch
        self.null = gaia_xmatch.Gaia_ID.isnull()
        self.gaia_info = self.initialise_result_df()
        self.error = []

    def initialise_result_df(self):
        # Test query to set up the result dataframe 
        test_id = 'Gaia EDR3 5022972468946212352' #Random example

        catalog_data = Catalogs.query_object(test_id, catalog="Gaia", radius = 0.001)
        df = catalog_data.to_pandas()

        d = df.copy()
        d.insert(0, 'groups_index', 1)
        d.insert(1, 'input_id', 'test')

        return d.drop(0)

    def query_gaia(self, r = 0.01):
        for i, gaia_id in enumerate(self.gaia_xmatch.Gaia_ID):

            # if i%100 == 0:
            #     print('--------------------')
            #     print('Saving')
            #     self.gaia_info.to_pickle('xmatch-gaia-r0_01.pkl')
            #     np.save('err_r0_01.npy', self.error)
            #     print('Saved')
            #     print('--------------------')
            
            # Exceptions
            if self.null[i] == True:
                continue
            if gaia_id == '':
                continue

            print(i,'----{}%'.format(round(i/len(self.gaia_xmatch)*100, 2)))

            try:
                catalog_data = Catalogs.query_object(gaia_id, catalog="Gaia", radius = r)
                data = catalog_data.to_pandas()
                try:
                    data = data.loc[[0]]
                    data.insert(0, 'groups_index', i)
                    data.insert(1, 'input_id', gaia_id)

                    self.gaia_info = pd.concat([self.gaia_info, data])
                    self.gaia_info = self.gaia_info.reset_index(drop = True)
                except:
                    # Save index of failed matches
                    self.error.append(i) 
                    print('Could not find a match')
                    continue
            except:
                self.error.append(i) 
                print('No clue what happened...')
                continue
        self.gaia_info.to_pickle('gaia-r0_01.pkl')
        np.save('err_r0_01.npy', self.error)