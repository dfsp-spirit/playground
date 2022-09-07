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

stc = read_source_estimate(fname_stc, subject='sample')

do_plot = False

if do_plot:
    # Define plotting parameters
    surfer_kwargs = dict(
        hemi='lh', subjects_dir=subjects_dir,
        clim=dict(kind='value', lims=[8, 12, 15]), views='lateral',
        initial_time=0.09, time_unit='s', size=(800, 800),
        smoothing_steps=5)

    # Plot surface
    brain = stc.plot(**surfer_kwargs)

    # Add title
    brain.add_text(0.1, 0.9, 'SourceEstimate', 'title', font_size=16)

## Look at data


shape = stc.data.shape
print('The data has %s vertex locations with %s sample points each.' % shape)

shape_lh = stc.lh_data.shape
print('The left hemisphere has %s vertex locations with %s sample points each.'
      % shape_lh)

is_equal = stc.lh_data.shape[0] + stc.rh_data.shape[0] == stc.data.shape[0]

print('The number of vertices in stc.lh_data and stc.rh_data do ' +
      ('not ' if not is_equal else '') +
      'sum up to the number of rows in stc.data')

peak_vertex, peak_time = stc.get_peak(hemi='lh', vert_as_index=True, time_as_index=True)
peak_vertex_surf = stc.lh_vertno[peak_vertex]

peak_value = stc.lh_data[peak_vertex, peak_time]

if do_plot:
    brain = stc.plot(**surfer_kwargs)

    # We add the new peak coordinate (as vertex index) as an annotation dot
    brain.add_foci(peak_vertex_surf, coords_as_verts=True, hemi='lh', color='blue')

    # We add a title as well, stating the amplitude at this time and location
    brain.add_text(0.1, 0.9, 'Peak coordinate', 'title', font_size=14)

lh_coordinates = stc[0]['rr'][stc.lh_vertno]
lh_data = stc.lh_data

rh_coordinates = stc[1]['rr'][src[1]['vertno']]
rh_data = stc.rh_data

