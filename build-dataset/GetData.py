"""
Created on Wed Jul  7 11:54:11 2021
Updated last: 22/01/2023
@author: Raphael Bendahan-West

description: Get metadata + spectra/wavelength from fits files 
"""
import pandas as pd
import numpy as np
from astropy.io import fits
import sys, os

class GetSpectra():
    
    CaIIK = 3933.66 #Ca II K line in Angstrom
    CaIIH = 3968.47 #Ca II H line in Angstrom
    
    def __init__(self, nb_files = None, length_spec = None, loaded_sK = None, loaded_sH = None):
        
        # Option to ammend downloaded spectra by loading the spectrum arrays
        if loaded_sK is not None and loaded_sH is not None:
            self.sK = loaded_sK
            self.sH = loaded_sH

            # prevents wavelengths to be calculated/loaded
            self.wave_initK = True 
            self.wave_initH = True 


        # Initialising arrays only if length is specified
        if length_spec is not None and nb_files is not None:
            self.sK = np.zeros([nb_files, length_spec])
            self.sH = np.zeros([nb_files, length_spec])

            self.wK = np.zeros(length_spec)
            self.wH = np.zeros(length_spec)

            self.rvK = np.zeros(length_spec)
            self.rvH = np.zeros(length_spec)

            # Flag when wavelength+rv have been calculated and stored
            self.wave_initK = False # Same arrays for every spectrum
            self.wave_initH = False # Same arrays for every spectrum

        self.corrupt = pd.DataFrame(data={'File':[]})
        self.corrupt_s = pd.DataFrame(data={'File':[]})

    # def clean_data(self):
    #     ''' Clean the data from corrupt files'''
    #     return
    
    def save_arr(self, s_path, w_path):
        self.corrupt.to_pickle(s_path + 'corrupt.pkl')
        np.save(s_path + 'sK.npy', self.sK)
        np.save(s_path + 'sH.npy', self.sH)

        if os.path.exists(w_path) == False:
            os.mkdir(w_path)
        
            np.save(w_path + 'wK.npy', self.wK)
            np.save(w_path + 'rvK.npy', self.rvK)

            np.save(w_path + 'wH.npy', self.wH)
            np.save(w_path + 'rvH.npy', self.rvH)

    def update_archive(self, index, file, keys, df):
        lines = [self.CaIIH, self.CaIIK]
        try:
            with fits.open(file) as h:
                if (h[0].header['WAVELMIN'] < self.CaIIH/10 < h[0].header['WAVELMAX']) & (h[0].header['WAVELMIN'] < self.CaIIK/10 < h[0].header['WAVELMAX']):
                    
                    for line in lines:
                        self.get_spec(file, line, index)

                    vals = self.get_meta(h, keys)

                    updated_df = pd.DataFrame(np.insert(df.values, index, values=vals, axis=0))
                    updated_df.columns = df.columns
                
                else:
                    vals = np.zeros(len(keys))
                    checked = True
                    vals = np.append(vals,checked)

                    updated_df = pd.DataFrame(np.insert(df.values, index, values=vals, axis=0))
                    updated_df.columns = df.columns

                    self.sK = np.insert(self.sK, index, np.zeros(2000), axis=0)
                    self.sH = np.insert(self.sH, index, np.zeros(2000), axis=0)

                    self.corrupt.loc[index] = [file]

        except:
            vals = np.zeros(len(keys))
            checked = True
            vals = np.append(vals,checked)

            updated_df = pd.DataFrame(np.insert(df.values, index, values=vals, axis=0))
            updated_df.columns = df.columns

            self.sK = np.insert(self.sK, index, np.zeros(2000), axis=0)
            self.sH = np.insert(self.sH, index, np.zeros(2000), axis=0)

            self.corrupt.loc[index] = [file]

        return updated_df

    def get_spec(self, file, wave, idx):

        wavelength, spec, error = fits.getdata(file)[0]
        condition = np.where(np.round(wavelength, 2) == wave)[0][0] # to get actual value

        if wave == self.CaIIK:
            self.sK = np.insert(self.sK, idx, spec[condition-1000:condition+1000], axis=0)

        elif wave == self.CaIIH:
            self.sH = np.insert(self.sH, idx, spec[condition-1000:condition+1000], axis=0)

        else:
            print('Wrong line')
            sys.exit()

        return

    def get_meta(self, h, keys):
        checked = False
        val = []

        for k in keys:
        
            if k == 'HIERARCH ESO TEL TARG ALPHA':
                s1,s2 = str(h[0].header[k]).split('.')
                s1 = self.pads(s1)
                d = float(s1[:-4])*360/24 + float(s1[-4:-2])/60*15 + float(s1[-2:]+'.'+s2)/3600*15 #Check again what data looks like
                val.append(d)
            
            elif k == 'HIERARCH ESO TEL TARG DELTA':
                s1,s2 = str(h[0].header[k]).split('.')
                sg = np.sign(float(s1))
                s1 = str(np.abs(int(s1)))
                s1 = self.pads(s1)
                d = sg*float(s1[:-4]) + sg*float(s1[-4:-2])/60 + sg*float(s1[-2:]+'.'+s2)/3600 #Check again what data looks like
                val.append(d)

            elif k == 'DATE-OBS':
                d = pd.to_datetime(h[0].header[k])
                val.append(d)

            else:
                val.append(h[0].header[k])

        checked = True
        val.append(checked)

        return val
        

    def get_spectrum(self, index, file):
        ''' Update function by creating new function that does metadata + spectra
        Only opens the file once and not for both'''
        lines = [self.CaIIH, self.CaIIK]
        # print(index, file)

        try:
            with fits.open(file) as h:
                for line in lines:
                    if h[0].header['WAVELMIN'] < line/10 < h[0].header['WAVELMAX'] :
                
                        wavelength, spec, error = fits.getdata(file)[0]
                        # print(line)
                        # print(np.where(wavelength == line))
                        condition = np.where(np.round(wavelength, 2) == line)[0][0] # to get actual value

                        if line == self.CaIIK:
                            self.sK[index,:] = spec[condition-1000:condition+1000]

                            if self.wave_initK is False:
                                self.wK = wavelength[condition-1000:condition+1000]
                                self.rvK = 3e5 * (self.wK-line)/(line)

                                self.wave_initK = True

                        elif line == self.CaIIH:
                            self.sH[index,:] = spec[condition-1000:condition+1000]

                            if self.wave_initH is False:
                                self.wH = wavelength[condition-1000:condition+1000]
                                self.rvH = 3e5 * (self.wH-line)/(line)

                                self.wave_initH = True
                        
                        else:
                            print('Wrong line')
                            sys.exit()

                    else:
                        print('error a')
                        self.corrupt_s.loc[index] = [file]
                        
        except:
            print('error b')
            self.corrupt_s.loc[index] = [file]
                
        return

    def pads(self, s1):
        if len(s1) < 6:
            pad = '0' * ( 6 - len(s1) )
            s1 = pad + s1
        return s1

    def get_metadata(self, index, file, keys, main_df):
       
        checked = False
        
        try:
            with fits.open(file) as h:
                if (h[0].header['WAVELMIN'] < self.CaIIH/10 < h[0].header['WAVELMAX']) & (h[0].header['WAVELMIN'] < self.CaIIK/10 < h[0].header['WAVELMAX']):
                    val = []

                    for k in keys:
                    
                        if k == 'HIERARCH ESO TEL TARG ALPHA':
                            s1,s2 = str(h[0].header[k]).split('.')
                            s1 = self.pads(s1)
                            d = float(s1[:-4])*360/24 + float(s1[-4:-2])/60*15 + float(s1[-2:]+'.'+s2)/3600*15 #Check again what data looks like
                            val.append(d)
                        
                        elif k == 'HIERARCH ESO TEL TARG DELTA':
                            s1,s2 = str(h[0].header[k]).split('.')
                            sg = np.sign(float(s1))
                            s1 = str(np.abs(int(s1)))
                            s1 = self.pads(s1)
                            d = sg*float(s1[:-4]) + sg*float(s1[-4:-2])/60 + sg*float(s1[-2:]+'.'+s2)/3600 #Check again what data looks like
                            val.append(d)

                        elif k == 'DATE-OBS':
                            d = pd.to_datetime(h[0].header[k])
                            val.append(d)

                        else:
                            val.append(h[0].header[k])

                    checked = True
                    val.append(checked)

                    main_df.loc[index] = val

                else:
                    val = np.zeros(len(keys))
                    checked = True
                    val = np.append(val,checked)
                    main_df.loc[index] = val
                    self.corrupt.loc[index] = [file]
            
            # return status
        
        except:
            val = np.zeros(len(keys))
            checked = True
            val = np.append(val,checked)
            main_df.loc[index] = val
            self.corrupt.loc[index] = [file]
            # return status
        
        return main_df