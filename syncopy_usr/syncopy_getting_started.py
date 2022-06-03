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


def perform_freq_analysis():
    """Perform frequency space analysis
    """
    data = get_test_data()
    #data.singlepanelplot(trials=0, toilim=[0, 0.5])    # Plot data

    ## Perform Multitapered Fourier Analysis
    fft_spectra = spy.freqanalysis(data, method='mtmfft', foilim=[0, 60], tapsmofrq=1)
    fft_spectra.singlepanelplot(trials=3) # Plot results

    ## Perform Wavelet Analysis
    fois = np.arange(10, 60, step=2) # frequencies to scan, 2Hz stepping
    wav_spectra = spy.freqanalysis(data,
                                method='wavelet',
                                foi=fois,
                                parallel=True, # requires cluster/SLURM for parallel=TRUE
                                keeptrials=False)
    wav_spectra.multipanelplot()  # Plot results


def dataset_arithmetic_and_preprocessing():
    """_summary_
    """
    data = get_test_data()
    import syncopy.tests.synth_data as spy_synth

    # a linear trend, requires dev branch as of June 2022
    lin_trend = spy_synth.linear_trend(y_max=3,
                                    nTrials=50,
                    samplerate=500,
                    nSamples=1000,
                    nChannels=2)
    
    # a 2nd 'nuisance' harmonic, also requires dev branch as of June 2022
    harm50 = spy_synth.harmonic(freq=50,
                                nTrials=50,
                    samplerate=500,
                    nSamples=1000,
                    nChannels=2)

    # add the data together, works due to equal dims
    data_nui = data + lin_trend + harm50
    # also works for scalars
    data_nui = data_nui + 5

    # perform spectral analysis of confounded data.
    cfg = spy.StructDict()
    cfg.tapsmofrq = 1
    cfg.foilim = [0, 60]
    cfg.polyremoval = None
    cfg.keeptrials = False   # trial averaging
    fft_nui_spectra = spy.freqanalysis(data_nui, cfg)

    # check the dirty results:
    fft_nui_spectra.singlepanelplot()

    # now pre-proc the data to remove confounds
    data_pp = spy.preprocessing(data_nui,
                            filter_class='but',
                            filter_type='lp',
                            polyremoval=1,
                            freq=40,
                            order=12)

    # and inspect the results of the analysis of the
    #  pre-processed data for comparison:
    spec_pp = spy.freqanalysis(data_pp, cfg)
    spec_pp.singlepanelplot()



if __name__ == "__main__":
    #perform_freq_analysis()
    dataset_arithmetic_and_preprocessing()
