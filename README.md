Automated Search for Spectroscopic Exocomet Transits
Using the HARPS archive
===
**Context**:
---
Exocomets are analogues of solar system comets, with the main difference being that they orbit stars other than the Sun. These extrasolar comets can be thought of as small icy planetesimals that were left unused during the planet formation phase of a system. Although being “leftover” dust agglomerates, exocomets tend to be part of the most pristine objects in a system, enclosing primordial information about the early phases of planetary formation.

An exocomet detection in spectroscopy is identified by variable absorption features around atomic lines in a stellar spectrum which can be explained by the exocometary gas transiting in front of a star. This project is designed to search for any transient absorption features in the ionised Calcium K (CaII K) line of HARPS spectra.

**Data used**: Entire [HARPS archive](http://archive.eso.org/wdb/wdb/adp/phase3_main/form) (from 21/03/2022)  
**Goal**: Estimate the frequency of observing exocomet transits in spectroscopy (CaII K line)

**Installation**
---
__TODO:__ *Change to python environment*  
```shell
python3 -m venv exocomet
source exocomet/bin/activate
```
Install dependencies:
```shell
# pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```