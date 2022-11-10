#!/usr/bin/env python3
#
# To use this, you will need to install MNE-Python like this:
# conda create -c conda-forge -y --name mne-test python=3.10 mne
# conda activate mne-test
#

import sys

from qtpy import QtWidgets

import pyvistaqt
import pyvista as pv


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    plotter = pyvistaqt.BackgroundPlotter()
    plotter.add_mesh(pv.Sphere(), smooth_shading=True)
    sys.exit(app.exec_())
