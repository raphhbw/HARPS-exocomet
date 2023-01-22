asset:
Automated Search for Spectroscopic Exocomet Transits
===
**Context**:  
Exocomets are analogues of solar system comets, with the main difference being that they orbit stars other than the Sun. These extrasolar comets can be thought of as small icy unused building blocks in planet formation. Although being “leftover” dust agglomerates, exocomets tend to be part of the most pristine objects in a system, enclosing primordial information about the early phases of planetary formation.

**Data**: Entire [HARPS archive](http://archive.eso.org/wdb/wdb/adp/phase3_main/form) (from 21/03/2022)  
**Goal**: Estimate the frequency of observing exocomet transits  

**asset**:  
Automated algorithm searching for transient absorption features around the ionised Calcium doublet (CaII).

**Potential changes**:
* Interested in variability around other atomic lines?  
  Change the `CaII_H` and `CaII_K` parameters to the desired line.
* Interested in using data from other spectroscopic instruments? (only for high resolution instruments)  
  Search component is independent of the instrument and should work with any spectra.

**Dependencies**  
__TODO:__ *Change to python environment when have time*  
```shell
conda create --name asset --file requirements.txt
conda activate asset
conda deactivate asset
```