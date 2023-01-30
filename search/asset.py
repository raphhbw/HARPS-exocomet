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

    def __init__(self, parameters = None):
        'initialise with param.json when we want to perform search'
        self.df = None
        self.target_red = None
        self.target_san = None
        self.target_harps = None

        self.sK = None
        self.err_sK = None

        self.w_H = None
        self.w_K = None
        
        self.rv_H = None
        self.rv_K = None

        self.snr_idxrange_K = None

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

        self.sK = np.load(star_path+'spec/sK.npy')

        self.w_H = np.load(star_path + 'wavelength/wH.npy')
        self.w_K = np.load(star_path + 'wavelength/wK.npy')
        
        self.rv_H = np.load(star_path + 'wavelength/rvH.npy')
        self.rv_K = np.load(star_path + 'wavelength/rvK.npy')

        if init == True:
            self.snr_idxrange_K = np.where((self.rv_K > self.rv_min) & (self.rv_K < self.rv_max))

    def snr_cutoff(self):
        snr = self.df.SNR.to_numpy()
        self.df = self.df[snr > self.snr_cut].reset_index(drop = True)
        self.sK = self.sK[snr > self.snr_cut]

    def std_cutoff(self, spec):
        med, _ = self.ref(spec)
        self.spec_err(med, spec)
        # print(self.err_sK)

        n_spec= spec[self.err_sK <= 1]
        self.df = self.df[self.err_sK <= 1].reset_index(drop = True)
        return n_spec

    def noise_cut(self, spec):
        ref, _ = self.ref(spec)
        cutoff = np.median(ref) * 0.25

        self.spec_err(ref, spec)
        new = spec[self.err_sK <= cutoff]
        self.df = self.df[self.err_sK <= cutoff].reset_index(drop = True)
        return new        

    def norm(self,rv,s):
        ''' Normalise the input spectrum array
        Returns array same shape as input
        '''
        ok = []
        norm_s = np.zeros_like(s)
        
        for i in range(len(rv)): #Finding indices of values in the conditions
            if rv[i] < -100:
                ok.append(i)
            if rv[i] > 100:
                ok.append(i)
            continue
        
        for i in range(len(s)): #Normalising all spectra
            spec = s[i,:]
            mean = np.mean(spec[ok])
            norm_s[i,:] = spec/mean
        
        return norm_s

    def ref(self, spectrum):
        '''Calculates reference spec'''
        median = np.median(spectrum, axis = 0)
        std =  np.std(spectrum, axis = 0)
        
        return median, std
    
    def spec_err(self, ref, s):
        self.err_sK = np.std(np.subtract(s, ref), axis=1)

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

        self.load_info(star)

        if len(self.df) <= 1:
            return None

        if snr_filt == True:
            self.snr_cutoff()

        norm_sK = self.norm(self.rv_K, self.sK)
        new_sK = self.smoothing(norm_sK, self.pts_filter)

        # new_sK = self.std_cutoff(new_sK)
        new_sK = self.noise_cut(new_sK)

        if len(self.df) <= 1:
            return None

        med,med_err = self.ref(new_sK)
        self.spec_err(med,new_sK)
        cond = (self.rv_K > -100) & (self.rv_K < 100)
        filtered_med = med[cond]

        if len(np.where(filtered_med > self.cutoff)[0]) > 0: #Changed to cutoff when MED (not spectrum) is >cutoff
            self.ccf = True
            # return None
        # else:
        #     return None

        return [new_sK, med, med_err]

    def get_width(self, sig):

        idx_min = np.nanargmin(sig)
        # print(width_depth.left(idx_min, sig), width_depth.right(idx_min, sig))
        width = width_depth.left(idx_min, sig) + width_depth.right(idx_min, sig) + 1 # +1 comes from the initial detection
                                                                # 1 data point = 1km/s width
        return width

    def X_corr(self, med):
        tw = np.linspace(self.w_K.min(), self.w_K.max(), 2000)
        tf = np.exp(-(tw-(self.Ca_K*10))**2/(2.*0.2**2))

        cond = (self.rv_K > -100) & (self.rv_K < 100)
        rv = self.rv_K[cond]
        corr = signal.correlate(med[cond], tf[cond], mode='same')
        rv_shift = rv[np.argmax(corr)]
        
        return rv_shift

    def quicksearch(self, star):
        ''' Quick search given target information 
            Returns name of the target if it is a candidate
                    None if not a candidate '''
        self.ccf = False
        spec_param = self.spec_analysis(star)

        if spec_param == None:
            return None
        else:
            new_sK, med, med_err = spec_param

        # if self.check_otypes == 1:
        #     otype = self.filter_otypes(self.target_san)
            
        #     if otype == None:
        #         return None
        
        # CCF
        corr_med = med.copy()
        if self.ccf == True:
            rv_shift = self.X_corr(corr_med)
            cond100 = (self.rv_K > rv_shift-50) & (self.rv_K < rv_shift+50)
            # corr_med[cond100] = np.nan

        for i in range(len(new_sK)):

            spec = new_sK[i]
            # corr_spec = spec.copy()
            # if self.ccf:
            #     corr_spec[cond100] = np.nan
            
            snr = self.snr(spec, med, self.err_sK[i], med_err)
                
            sd = np.std(snr)

            corr_snr = snr.copy()
            if self.ccf == True:
                corr_snr[cond100] = np.nan
            corr_snr = corr_snr[self.snr_idxrange_K]

            # new_snr = snr[self.snr_idxrange_K]

            # sig = new_snr/sd
            sig = corr_snr/sd

            min_detect = np.nanmin(sig)

            if min_detect < self.threshold:
                width = self.get_width(sig)
                if width >= self.width_filter:
                    return self.target_red
        
        return None
        
