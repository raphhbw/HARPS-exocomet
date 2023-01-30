Automated Search for Spectroscopic Exocomet Transits
Using the HARPS archive
===
**Context**:
---
Exocomets are analogues of solar system comets, with the main difference being that they orbit stars other than the Sun. These extrasolar comets can be thought of as small icy planetesimals that were left unused during the planet formation phase of a system. Although being “leftover” dust agglomerates, exocomets tend to be part of the most pristine objects in a system, enclosing primordial information about the early phases of planetary formation.

An exocomet detection in spectroscopy is identified by variable absorption features around atomic lines in a stellar spectrum which can be explained by the exocometary gas transiting in front of a star. This project is designed to search for any transient absorption features in the ionised Calcium K (CaII K) line of HARPS spectra.

**Data used**: Entire [HARPS archive](http://archive.eso.org/wdb/wdb/adp/phase3_main/form) (from 21/03/2022)  
**Goal**: Estimate the frequency of observing exocomet transits in spectroscopy (CaII K line)

**Install dependencies**
---
```shell
conda create --name exocomet --file requirements.txt
conda activate exocomet
```

**How to run**
---
_build-dataset_:  
1. `metadata.py` - saves metadata from fits files in `fits` folder, using `GetData.py`
2. `spectra.py` - saves spectra from fits files in `fits` folder for specified atomic line (CaII H & K lines), using `GetData.py`.  
+/- 2000 points from atomic line is saved
3. `santise_reduce.py` - cleans up the name of the observed targets to facilitate grouping (eg. 'reduced' name is all lower case and underscore, dashes, spaces are removed)

_groups_:  
4. `grouping.py` - group observed targets by 'reduced' name and coordinates
5. `create_dataset.py` - create `dataset` folder with all the stars in subfolders with `reduced` name

_HR_:  
6. `Gaia.py` - get Gaia IDs and then query Gaia Catalogue to get information for HR diagram

_search_:  
Both use `param.json` as parameters for the search.
7. `quicksearch.py` - searches through dataset for exocomet transits and returns a list of potential candidates
8. `iplotter.py` - different options (check `iplotter.py --help`):
    - `--star <name>` - will show interactive diagnostic plots for this specific star
    - no options - will run through results of `quicksearch.py` and show interactive diagnostic plots for star satisfying `param.json`

The interactive diagnostic plots will ask for user input to:
- classify stars - classification will be visible in `results/CandidateReport/`:
    - 'candidate' - press `y`
    - 'not_candidate_but_real' - press `n`
    - 'not_candidate_but_junk' - press `j`
    - 'flagged' - press `w`
    - 'skip' - press `space`
- print all metadata for the spectra of the star - press `d`
- print metadata for all the potential detections - press `o`

After classification done, close the plot and the next star should pop up. At the end you will have the option to review skipped stars and flagged stars.