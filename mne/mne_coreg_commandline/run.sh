#!/bin/sh
#
# Shell script illustration head model and forward computation with MNE.
#
# See https://mne.tools/dev/auto_tutorials/forward/30_forward.html
# for details.

# Computing the forward operator requires:
#
# * a `*-trans.fif` file that contains coregistration info: this file is output by coregistraion of sensors and sMRI image, using interactive MNE GUI.
# * a source space: either surface-based or volume based. derived from FreeSurfer sMRI-output (surface mesh) by using a subset of the vertices.
# * the BEM surfaces: these can be computed from FreeSurfer output using MNE in Python, or the `mne watershed_bem` command line tool.

export FREESURFER_HOME="${HOME}/software/freesurfer"
export SUBJECTS_DIR="${HOME}/data/MEG4Syncopy/MRI/freesurfer_run"
export SUBJECT="subject1"

## Create the BEM surfaces (outer skull, inner skull, ) for the head model.
mne watershed_bem -d ${SUBJECTS_DIR} -s ${SUBJECT}

