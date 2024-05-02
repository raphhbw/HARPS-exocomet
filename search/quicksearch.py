'''
30/08/22
QuickSearch returns numpy array of candidate target names.
Search done according to parameters in param.json
'''
import time
import numpy as np
import glob, os, sys
from asset import ASSET
import multiprocessing
import json, argparse

if __name__ == '__main__':
    startTime = time.time()

    parser = argparse.ArgumentParser(description='How to use QuickSearch', epilog='ASSET by RBW')
    parser.add_argument('--p', metavar='param.json', default='param.json', help='parameter file name (default:param.json)')
    parser.add_argument('--nice', metavar='niceness', default=15, help='niceness of job (default: 15)')
    parser.add_argument('--line', metavar='line', default='K', help='define what atomic line to use (default: "K")')
    parser.add_argument('--r', metavar='res-path', default='../results/QuickSearch/', help='output path (default: ../results/QuickSearch/)')

    args = parser.parse_args()

    os.nice(int(args.nice))

    with open(args.p) as paramfile:
        param = json.load(paramfile)

    dataset_path = glob.glob(param["dataset"] + '*/')

    # print(len(dataset_path))
    # sys.exit()

    Search = ASSET(parameters=param, line=args.line)

    with multiprocessing.Pool(param["cores"]) as pool:
        out = pool.map(Search.quicksearch, dataset_path)

    output = np.array(out)
    print('------------------')
    # print(output.sum())
    # print('tot: {}, removed {}'.format(Search.tot_spec, Search.tot_err_spec))

    cands = output[output != None]
    print(cands, len(cands))

    cands_file = 'candidates_{}sig_{}cut_{}width.npy'.format(Search.threshold, Search.cutoff, Search.width_filter)

    if not os.path.exists(args.r):
        os.makedirs(args.r)
        print("new directory {} created!".format(args.r))

    np.save(args.r + cands_file, cands)

    executionTime = (time.time() - startTime)
    print('Execution time in seconds: ' + str(executionTime))
    # print('Number of stars with <= 1 spectrum:', Search.count_df_1)