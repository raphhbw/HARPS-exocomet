import pandas as pd
import numpy as np

class HR_Diagram():

    def __init__(self):
        gaia_xmatch = []
        groups = []
        self.load_df()

    def load_df(self):
        self.gaia_xmatch = pd.read_pickle('../HR/gaia-r0_01.pkl')
        self.groups = pd.read_pickle('../build-dataset/res/meta/groups_w_gaia.pkl')

    def build_HR(self, in_df, adjust = True):

        if adjust == True:
            gaia_info = self.adjust_df(in_df)
        else:
            gaia_info = in_df

        return self.HRparam(gaia_info)

    def adjust_df(self, df):
        ''' Removing the stars with:
        * -ve parallax
        * Plx error bigger than 5%
        * G-Rp = 0
        * TODO G-Rp error bigger than 5% '''
        
        
        idx1 = df[df['parallax']<0].index.values
        idx2 = df[df['parallax_error'] > df['parallax']*0.05].index.values
        idx3 = df[df['g_rp'] == 0].index.values
        # idx4 = df[np.sqrt(df['phot_g_mean_mag_error']**2 + df['phot_rp_mean_mag_error']) > 0.05].index.values
        
        idx = np.concatenate((idx1,idx2,idx3))
        # idx = np.concatenate((idx1,idx2, idx3, idx4))
        # print(idx)
        
        df = df.drop(idx)
        df = df.reset_index(drop=True)
        
        return df

    def HRparam(self, df):
        ''' Get the relevant info from gaia catalogue to build HR '''
    
        colour   = df['g_rp']
        app_mag  = df['phot_g_mean_mag']
        parallax = df['parallax']
        # plx_err  = df['parallax_error']
        # TODO get G-Rp error
        # x_err    = np.sqrt(df['phot_g_mean_mag_error']**2 + df['phot_rp_mean_mag_error'])
        # sep      = df['Separation']
        
        Mag = app_mag - 5*(np.log10(1000/parallax)-1) #parallax is in mas!
        # Mag_err = np.sqrt((Mag - (app_mag - 5*(np.log10(1/(parallax + plx_err))-1)))**2)
        
        # return colour, Mag, Mag_err
        return colour, Mag

    def get_star_gaia_info(self, star):
        ''' Get Gaia info from reduced name of a candidate '''

        idx = self.groups[self.groups.Reduced == star].index.values[0]
        star_gaia = self.gaia_xmatch[self.gaia_xmatch.groups_index == idx]

        return star_gaia