Automated Search for Spectroscopic Exocomet Transits
Using HARPS spectra
===

Run an automated search for exocomet transits from raw HARPS 2D fits files.

**Data used in paper**: Entire [HARPS archive](http://archive.eso.org/wdb/wdb/adp/phase3_main/form) (from 21/03/2022)  

**List of dependencies**
---
All package dependencies can be found listed in `requirements.txt`.

**How to run**
---
If you have a folder with fits files corresponding to different stars, this is how we created our database:  
_build-dataset_:  
1. `metadata.py` - saves metadata from fits files in `fits` folder, using `GetData.py`
2. `spectra.py` - saves spectra from fits files in `fits` folder for specified atomic line (CaII H & K lines), using `GetData.py`. +/- 2000 points from atomic line is saved
3. `sanitise_reduce.py` - cleans up the name of the observed targets to facilitate grouping (eg. 'reduced' name is all lower case and underscore, dashes, spaces are removed)

_groups_:  
1.  `grouping.py` - group observed targets by 'reduced' name and coordinates  
2.  `create_dataset.py` - create `dataset` folder with all the stars in subfolders with `reduced` name  


Code that we used to generate our vetting plots use the following codes. Note these will need to be adjusted to your own database:  
_HR_:  
1. `Gaia.py` - get Gaia IDs and then query Gaia Catalogue to get information for HR diagram

_search_:  
Both use `param.json` as parameters for the search.  
1. `quicksearch.py` - searches through dataset for exocomet transits and returns a list of potential candidates  
2. `iplotter.py` - different options (check `iplotter.py --help`):  
    - `--star <name>` - will show interactive diagnostic plots for this specific star  
    - no options - will run through results of `quicksearch.py` and show interactive diagnostic plots for star satisfying `param.json`

The interactive diagnostic plots will ask for user input to:
- classify stars - classification results will be visible in `results/CandidateReport/`:  
    - 'candidate' - press `y`  
    - 'not_candidate_but_real' - press `n`  
    - 'not_candidate_but_junk' - press `j`  
    - 'flagged' - press `w`  
    - 'skip' - press `space`  
- print all metadata for the spectra of the star - press `d`
- print metadata for all the potential detections - press `o`

After classification done, close the plot and the next star should pop up. At the end you will have the option to review skipped stars and flagged stars.
