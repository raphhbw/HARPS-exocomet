import pandas as pd
from astroquery.simbad import Simbad

def get_otypes(star):

    # Custom Simbad search
    custom_simbad = Simbad()
    custom_simbad.get_votable_fields()
    custom_simbad.add_votable_fields('otypes', 'rv_value', 'otype', 'plx', 'sp')
    custom_simbad.get_votable_fields()
    custom_simbad.remove_votable_fields('coordinates')
    custom_simbad.get_votable_fields()

    sim = custom_simbad.query_objects([star])
    # print(sim)
    # print('-------yooooooooooooo')
    try:
        df = sim.to_pandas()
        df = df.drop(columns=['SCRIPT_NUMBER_ID'])
        return df
    except:
        # print('No match with Simbad')
        return

    

# star = 'beta pic'
# print(get_otypes(star))