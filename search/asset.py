from statistics import mode

import numpy as np
import pandas as pd
from scipy import ndimage
from scipy import signal

import width_depth
from otypes import get_otypes


class ASSET():

    Ca_K = 393.366 #Ca II K line in nm
    Ca_H = 396.847 #Ca II H line in nm
    # undesired_otypes = ['RotV*alf2CVn', 'SB*', 'PulsV*delSct', 'RRLyr',
    #     'PulsV*bCep', 'V*', 'PulsV*', 'EB*', 'Seyfert_1', 'RotV*', 
    #     'Cepheid', 'EllipVar', 'PulsV*RVTau', 'gammaDor', 'HMXB', 'Nova']

    def __init__(self, line, parameters = None):
        '''initialise with param.json when we want to perform search
        options for line: either 'H' or 'K'
        '''
        self.df = None
        self.target_red = None
        self.target_san = None
        self.target_harps = None

        self.line = line

        self.spectra = None
        self.spectra_err = None
        self.wavelength = None #given in Angstrom
        self.radial_velocity = None

        self.tot_err_spec = []
        self.tot_spec = []

        self.ok = []

        self.snr_idxrange = None

        self.ccf = False #By default ccf flag is off - activated when act_cutoff on

        if parameters != None:
        
            self.threshold = parameters["threshold"]
            self.pts_filter = parameters["med_filter_bin"]
            self.rv_min = parameters["rv_min"]
            self.rv_max = parameters["rv_max"]
            self.cutoff = parameters["cutoff"]
            self.snr_cut = parameters["SNR_cut"]
            self.width_filter = parameters["width_filt"]


    def load_info(self, star_path, init = True):
        'Init goes to false when no search is done'
        self.df = pd.read_pickle(star_path+'meta/group_df.pkl')
        self.target_red = mode(self.df.Reduced)
        self.target_san = mode(self.df.Sanitised)
        self.target_harps = mode(self.df.Object)

        if self.line == 'K':
            self.spectra = np.load(star_path+'spec/sK.npy')
            self.wavelength = np.load(star_path + 'wavelength/wK.npy')
            self.radial_velocity = np.load(star_path + 'wavelength/rvK.npy')
        elif self.line == 'H':
            self.spectra = np.load(star_path+'spec/sK.npy')
            self.wavelength = np.load(star_path + 'wavelength/wK.npy')
            self.radial_velocity = np.load(star_path + 'wavelength/rvK.npy')
        else:
            return NotImplementedError

        if init == True:
            self.snr_idxrange = np.where((self.radial_velocity > self.rv_min) & (self.radial_velocity < self.rv_max))

    def snr_cutoff(self):
        snr = self.df.SNR.to_numpy()
        self.df = self.df[snr > self.snr_cut].reset_index(drop = True)
        self.spectra = self.spectra[snr > self.snr_cut]

    def noise_cut(self, spec):
        ''' Make an initial cut on spectra that are too noisy to observe a 4sigma signal '''
        ref, _ = self.ref(spec)
        new_ref = ref[self.ok]

        new_spectrum = spec[:,self.ok]
        # print(new_ref.shape, new_spectrum.shape)

        # Determine value that defines a 1sigma signal
        cutoff = np.median(new_ref) * 0.25

        # Determine error in each spectrum
        self.spec_err(new_ref, new_spectrum)
        new = spec[self.spectra_err <= cutoff]
        self.df = self.df[self.spectra_err <= cutoff].reset_index(drop = True)

        return new        

    def norm(self,rv,s):
        ''' Normalise the input spectrum array
        Returns array same shape as input
        '''
        self.ok = []
        norm_s = np.zeros_like(s)
        
        for i in range(len(rv)): #Finding indices of values in the conditions
            # if rv[i] < -100:
            if rv[i] < -200:
                self.ok.append(i)
            if rv[i] > 200:
            # if rv[i] > 100:
                self.ok.append(i)
            continue
        
        for i in range(len(s)): #Normalising all spectra
            spec = s[i,:]
            mean = np.mean(spec[self.ok])
            norm_s[i,:] = spec/mean
        
        return norm_s

    def ref(self, spectrum):
        '''Calculates reference spec and its error'''
        median = np.median(spectrum, axis = 0)
        std =  np.std(spectrum, axis = 0)
        
        return median, std
    
    def spec_err(self, ref, s):
        self.spectra_err = np.std(np.subtract(s, ref), axis=1)

    def smoothing(self, spec, pts):
        '''Smooting data using a rolling median filter
        Input 2D array of shape (x,2000)
        Return same shape array'''
        new_spec = ndimage.median_filter(spec, size=(1,pts), mode="nearest")
        return new_spec

    def snr(self, s, m, err_s, err_m):
        '''
        Input spec 1Darray, median ref
        Returns snr 1Darray of input 
        Calculates snr and adds noise in quadrature
        '''
        # new_std = np.std(s - m, axis = 0)
        noise = np.sqrt(err_s**2 + err_m**2)
        snr = (s - m)/noise
        return snr

    def spec_analysis(self, star, snr_filt = False):
        # Load necessary info for search e.g. spectra, wavelength...
        self.load_info(star)

        if len(self.df) <= 1:
            print('[{}] not enough spectra for the search!'.format(self.target_red))
            return None

        if snr_filt == True:
            self.snr_cutoff()

        # Normalise spectra
        norm_spectra = self.norm(self.radial_velocity, self.spectra)
        # Smooth spectra
        new_spectra = self.smoothing(norm_spectra, self.pts_filter)

        new_spectra = self.noise_cut(new_spectra)

        if len(self.df) <= 1:
            print('[{}] not enough spectra for the search after cutting noisy spectra!'.format(self.target_red))
            return None

        med, med_err = self.ref(new_spectra)
        self.spec_err(med,new_spectra)

        cond = (self.radial_velocity > -100) & (self.radial_velocity < 100)
        filtered_med = med[cond]

        # Checking for stellar activity i.e. strong emission +/- 100km/s from systemic velocity
        if len(np.where(filtered_med > self.cutoff)[0]) > 0: #Changed to cutoff when MED (not spectrum) is >cutoff
            self.ccf = True # Flag changed to No CCF
            # return None
        # else:
        #     return None

        return [new_spectra, med, med_err]

    def get_width(self, sig):

        idx_min = np.nanargmin(sig)
        # print(width_depth.left(idx_min, sig), width_depth.right(idx_min, sig))
        width = width_depth.left(idx_min, sig) + width_depth.right(idx_min, sig) + 1 # +1 comes from the initial detection
                                                                # 1 data point = 1km/s width
        return width

    def X_corr(self, med):
        tw = np.linspace(self.wavelength.min(), self.wavelength.max(), 2000)
        if self.line == 'K':
            tf = np.exp(-(tw-(self.Ca_K*10))**2/(2.*0.2**2))
        elif self.line == 'H':
            tf = np.exp(-(tw-(self.Ca_H*10))**2/(2.*0.2**2))
        else:
            return NotImplementedError

        cond = (self.radial_velocity > -100) & (self.radial_velocity < 100)
        rv = self.radial_velocity[cond]
        corr = signal.correlate(med[cond], tf[cond], mode='same')
        rv_shift = rv[np.argmax(corr)]
        
        return rv_shift

    def quicksearch(self, star):
        ''' Quick search given target information 
            Returns name of the target if it is a candidate
                    None if not a candidate '''
        self.ccf = False
        spec_param = self.spec_analysis(star)

        # if spec_param[1] == None:
        #     return spec_param[0]
        if spec_param == None:
            return None
        else:
            new_spectra, med, med_err = spec_param

        # if self.check_otypes == 1:
        #     otype = self.filter_otypes(self.target_san)
            
        #     if otype == None:
        #         return None
        
        # CCF
        corr_med = med.copy()
        if self.ccf == True:
            rv_shift = self.X_corr(corr_med)
            # select area +/- 50km/s from systemic velocity
            cond100 = (self.radial_velocity > rv_shift-50) & (self.radial_velocity < rv_shift+50)
            # corr_med[cond100] = np.nan

        for i in range(len(new_spectra)):

            spec = new_spectra[i]
            
            snr = self.snr(spec, med, self.spectra_err[i], med_err)
                
            sd = np.std(snr)

            corr_snr = snr.copy()
            if self.ccf == True:
                corr_snr[cond100] = np.nan
            corr_snr = corr_snr[self.snr_idxrange]
            
            sig = corr_snr/sd

            min_detect = np.nanmin(sig)

            if min_detect < self.threshold:
                # print('detection----------------------')
                width = self.get_width(sig)
                if width >= self.width_filter:
                    return self.target_red
        
        return None