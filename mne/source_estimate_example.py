#!/usr/bin/env python

# To use this, you will need to install MNE python. I recommend
# to create a new conda env with mne, activate it and then run
# this script in that environment.
#
# E.g.:
#
# conda create -y --name mne python=3.9
# conda activate mne
# conda install -y mne
#

from mne import read_source_estimate
from mne.datasets import sample


# Paths to example data
sample_dir_raw = sample.data_path()
sample_dir = sample_dir_raw / 'MEG' / 'sample'
subjects_dir = sample_dir_raw / 'subjects'


fname_stc = sample_dir / 'sample_audvis-meg'
