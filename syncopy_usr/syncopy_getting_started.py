# This follows the syncopy quickstart guide
# at https://syncopy.readthedocs.io/en/dev/quickstart/quickstart.html

import numpy as np
import syncopy as spy

def get_test_data():
    """Get synthetic syncopy data

    Returns:
        syncopy.AnalogData: the generated data
    """
    nTrials = 50
    nSamples = 1000
    nChannels = 2
    samplerate = 500   # in Hz

    # the sampling times vector needed for construction
    tvec = np.arange(nSamples) * 1 / samplerate
    # the 30Hz harmonic
    harm30 = np.cos(2 * np.pi * 30 * tvec)
    # linear dampening down to 10% of the original amplitude
    dampening = np.linspace(1, 0.1, nSamples)
    signal = dampening * harm30

    # collect trials
    trials = []
    for _ in range(nTrials):

        # we start with the white noise
        trial = np.random.randn(nSamples, nChannels)
        # now add the damped harmonic on the 1st channel
        trial[:, 0] += signal

        trials.append(trial)

    # instantiate Syncopy data object
    data = spy.AnalogData(trials, samplerate=samplerate)
    return data



data = get_test_data()
#data.singlepanelplot(trials=0, toilim=[0, 0.5])
fft_spectra = spy.freqanalysis(data, method='mtmfft', foilim=[0, 60], tapsmofrq=1)
