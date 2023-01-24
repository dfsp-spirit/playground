#!/usr/bin/env python

import os
import numpy as np
import syncopy as spy

# use syncopy

from syncopy.tests.test_metadata import _get_fooof_signal
st = "[SCRIPT]"

print(f"{st} Env var SPYLOGLEVEL is: '{os.getenv('SPYLOGLEVEL')}'.")
print(f"{st} Env var SPYLOGDIR is: '{os.getenv('SPYLOGDIR')}'.")
print(f"{st} Env var SPYTMPDIR is: '{os.getenv('SPYTMPDIR')}'.")

cfg = spy.get_defaults(spy.freqanalysis)
cfg.method = "mtmfft"
cfg.taper = "hann"
cfg.select = { "channel" : 0 }
cfg.keeptrials = False
cfg.output = "fooof"
cfg.foilim = [1., 100.]
cfg.parallel = True

print(f"{st} Generating input data.")
data = _get_fooof_signal()

print(f"{st} Running FOOOF.")
res = spy.freqanalysis(cfg, data)

print(f"{st} Done running FOOOF.")

# use mpi4py
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

print(f"{st} Trying mpi4py, my rank in MPI.COMM_WORLD is {rank}.")

# use some heat function

import heat
