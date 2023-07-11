import numpy as np
from GetData import GetSpectra
import glob

input_fits_path = "../fits/"

file_list = sorted(glob.glob(input_fits_path + 'ADP.*.fits'))

Spectra = GetSpectra(nb_files= len(file_list), length_spec= 2000) # 2000 points for 20 Angstrom

for i, file in enumerate(file_list):

    Spectra.get_spectrum(i, file)

    print('{}/{}'.format(i+1,len(file_list)))
    # sys.exit()
    
    if i%10000 == 0:
        Spectra.save_arr(s_path='res/spec/' , w_path='res/wavelengths/')

        
Spectra.save_arr(s_path='res/spec/' , w_path='res/wavelengths/')
print('Saved')
print('----------------------')
print(Spectra.corrupt)
print(Spectra.sK)