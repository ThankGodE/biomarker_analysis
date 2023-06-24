This script analysis biomarker clinical data. It runs on a python virtual environment with all libraries installed.

If you wish to use your own python version, please install the libraries in the requirements file.

Steps to use:

1. Activate python virtual environment in the code base

source biomarker_analysis/venv/bin/activate

2. Run script with the required arguments:

src/main/identify_biomarkers.py -o path_to_output_directory/ -i clinical.csv