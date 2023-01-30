import pandas as pd
import os, sys

class Classify():

    print_columns_d = ['index', 'Object', 'Sanitised', 'Reduced', 'Alpha', 'Delta', 
                    'SNR', 'Date', 'Epoch', 'RV', 'RA', 'Dec', 'New Groups', 'Min_SNR', 'RV_pos' ]

    print_columns_o = ['index', 'Object', 'Sanitised', 'Reduced', 'Alpha', 'Delta', 'SNR', 'Date',
     'Epoch', 'RV', 'RA', 'Dec', 'New Groups', 'Min_SNR', 'RV_pos', 'Abs_width', 'Abs_depth' ]

    def __init__(self, parameters, res_path):
        
        # self.param = [parameters["threshold"], parameters["med_filter_bin"],
        #                 parameters["rv_min"], parameters["rv_max"], parameters["SNR_cut"]]

        self.param = [parameters["threshold"], parameters["med_filter_bin"],
                        parameters["rv_min"], parameters["rv_max"], parameters["cutoff"],
                         parameters["width_filt"]]

        self.res_path = res_path
        self.cand_report_path = res_path + 'candidate_report.pkl'

        status = ['flagged', 'not_candidate_but_real', 'not_candidate_but_junk', 'candidate']

        for st in status:
            if os.path.exists(res_path + '{}/'.format(st)) == False:
                os.mkdir(res_path + '{}/'.format(st))

        if os.path.exists(self.cand_report_path):
            self.candidate_report = pd.read_pickle(self.cand_report_path)
        else:
            self.candidate_report = pd.DataFrame(data={'Target':[], 'Status':[], 'Parameters':[]}).astype(object)

        self.target_name = None
        self.target_info = None
        self.detection_info = None
        self.previous_report = None
        self.current_status = None

        self.skipped = []
        self.flagged = False
        # self.save_plot = False

    def candidate_info(self, target):
        ''' Load all information from a specific target.
            Return -> Has the target already been looked at? True/False '''
        
        self.current_status = None
        self.target_name = target
        # target_path = '../dataset/{}/'.format(target)
        # self.target_info = pd.read_pickle(target_path + 'meta/group_df.pkl')

        self.previous_report = self.candidate_report[self.candidate_report['Target'] == target]

        if len(self.previous_report) == 1:
            classified = True
            if 'flagged' in self.previous_report.Status.to_numpy(): # Checking if previously flagged
                self.flagged = True
            else:
                self.flagged = False
        elif len(self.previous_report) > 1:
            raise ValueError('Candidate:{} has more than one entry in the DataFrame.'.format(target))
        else:
            classified = False
            self.flagged = False

        return classified

    def classify(self):
        ''' Classify target according to its status - ie. candidate/not candidate/flagged'''

        if self.current_status == 'skipped':
            self.skipped.append(self.target_name)
            return None

        elif self.flagged is not True:
            cand_report = self.candidate_report
            cand_report.loc[len(cand_report.index)] = [self.target_name, self.current_status, self.param] # adding row at the bottom of the candidate report df
            self.candidate_report = cand_report.astype(object)

        else:
            # print(self.candidate_report)
            # print(self.previous_report)
            self.candidate_report.iloc[self.previous_report.index.values[0]]['Status'] = self.current_status
        
        return self.res_path + '{}/'.format(self.current_status)

    def onkey(self, event):
        ''' Set the different keys for Interactive Plot.
            Will have to give a status then quit plot to go to next target.
            If no status is given, the same target will be shown. '''

        if event.key == 'y': # Candidate
            self.current_status = 'candidate'
            print('{}: Currently CANDIDATE'.format(self.target_name))

        if event.key == 'n': # Not a candidate
            self.current_status = 'not_candidate_but_real'
            print('{}: Currently NOT A CANDIDATE: Real astrophysical variability'.format(self.target_name))

        if event.key == 'j': # Junk
            self.current_status = 'not_candidate_but_junk'
            print('{}: Currently NOT A CANDIDATE: Junk'.format(self.target_name))

        if event.key == 'w': # Flag
            self.current_status = 'flagged'
            print('{}: Currently FLAGGED'.format(self.target_name))
            
        if event.key == ' ': # Skip target
            self.current_status = 'skipped'
            print('{}: Currently SKIPPED'.format(self.target_name))

        if event.key == 'enter': # Quick save
            print('Saving progress...')
            self.candidate_report.to_pickle(self.cand_report_path)
            self.candidate_report.to_html(self.res_path + 'Report.html')
            print('Saved!')

        if event.key == 'escape': # Quit for the day with saving
            self.candidate_report.to_pickle(self.cand_report_path)
            self.candidate_report.to_html(self.res_path + 'Report.html')
            print('Saved!')
            sys.exit()

        if event.key == 'd': # Print the target's individual df
            print(self.target_info[self.print_columns_d])

        if event.key == 'o':
            print(self.detection_info[self.print_columns_o])
