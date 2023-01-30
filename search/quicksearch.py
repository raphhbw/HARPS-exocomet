'''
30/08/22
QuickSearch returns numpy array of candidate target names.
Search done according to parameters in param.json
'''
import time
import numpy as np
import glob, os
from asset import ASSET
import multiprocessing
import json, argparse

startTime = time.time()

parser = argparse.ArgumentParser(description='How to use QuickSearch', epilog='ASSET by RBW')
parser.add_argument('--p', metavar='param.json', default='param.json', help='parameter file name (default:param/param.json)')
parser.add_argument('--nice', metavar='niceness', default=15, help='niceness of job (default: 15)')
args = parser.parse_args()

os.nice(int(args.nice))

with open(args.p) as paramfile:
    param = json.load(paramfile)

dataset_path = glob.glob(param["dataset"] + '*/')

Search = ASSET(param)

with multiprocessing.Pool(param["cores"]) as pool:
    out = pool.map(Search.quicksearch, dataset_path)

output = np.array(out)

cands = output[output != None]

cands_file = 'candidates_{}_{}_{}sig_{}med_{}cut_width{}.npy'.format(Search.rv_min, Search.rv_max,
                Search.threshold, Search.pts_filter, Search.cutoff, Search.width_filter)

# cands_file = 'old_noise_filtering.npy'

np.save('../results/QuickSearch/' + cands_file, cands)

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))