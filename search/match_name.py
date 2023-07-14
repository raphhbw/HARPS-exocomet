import pandas as pd

def find_target(star):
    metadata = pd.read_pickle('../build-dataset/res/meta/full_metadata.pkl')
    group_dependency = pd.read_pickle('../build-dataset/res/meta/groups.pkl')

    group_df = metadata[metadata['Reduced'] == star].reset_index(drop = True)

    if len(group_df) > 0:
        # return group_dependency.loc[group_df['New Groups'][0]]
        return group_dependency.set_index('New Groups').loc[group_df['New Groups'][0]]
    else:
        raise FileNotFoundError

# target = 'betapic'

# try:
#     candidates = find_target(target)
#     print(candidates.Sanitised)
#     # print(find_target('betapic'))

# except FileNotFoundError:
#     print('Try again!')