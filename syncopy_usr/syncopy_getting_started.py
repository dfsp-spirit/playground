# This follows the syncopy quickstart guide
# at https://syncopy.readthedocs.io/en/dev/quickstart/quickstart.html
#
# Note that as of 2022-06, this tutorial requires the dev version of
# syncopy, which you need to install by cloning the GitHub repo and then
# installing it with `pip install -e .` into the conda environment you use.
#
# I would recommend cloning the ESI 'syncopy' environment and starting from
# there.

# %%

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


def connectivity_analysis():
    from syncopy.tests import synth_data

    # -----prepare data-----
    # we create two coupled autoregressive processes of order 2:
    nTrials = 50
    nSamples = 1500

    # 2x2 Adjacency matrix to define coupling
    AdjMat = np.zeros((2, 2))
    # coupling 0 -> 1
    AdjMat[0, 1] = 0.2


    data = synth_data.AR2_network(nTrials, samplerate=500, AdjMat=AdjMat, nSamples=nSamples)
    spec = spy.freqanalysis(data, tapsmofrq=3, keeptrials=False)
    # show oscillations
    data.singlepanelplot(trials=0, toilim=[0, 0.5])
    spec.singlepanelplot() # better visable in spectra

    # --- coherence -----
    # investigate channel relationships via coherence, based on spectra.
    coherence = spy.connectivityanalysis(data, method='coh', tapsmofrq=3)
    
    # visualize 2 (arbitrary) channel combinations from the result (we only have
    #  2 channels here, so it is actually the only one in this case).
    # note that coherence is symmetric, so we only show one of the (identical)
    # plots here
    coherence.singlepanelplot(channel_i='channel1', channel_j='channel2')
    #coherence.singlepanelplot(channel_i='channel2', channel_j='channel1')
    # coherence uses trial averaging, so we cannot look at individual channels.

    # --- cross correlation ---
    # now we look for channel relations in time-domain, using cross corr.
    corr = spy.connectivityanalysis(data, method='corr', keeptrials=True)
    # we look for 2 different trials here
    corr.singlepanelplot(channel_i=0, channel_j=1, trials=0)
    corr.singlepanelplot(channel_i=0, channel_j=1, trials=1)
    # note that there are correlations also for longer lags, and that no
    # trial averaging is done, so we can check trials.

    # --- Granger causality ---
    # investigate directionality/causality between channels.
    # uses Granger-Geweke algorithm for non-parametric Granger 
    # causality in the spectral domain.
    granger = spy.connectivityanalysis(data, method='granger', tapsmofrq=2)
    # in this case, we plot both directions, of course:
    granger.singlepanelplot(channel_i=0, channel_j=1)
    granger.singlepanelplot(channel_i=1, channel_j=0)
    # Granger causality also uses trial averaging, so we cannot look
    # at individual channels.

    # --- Save some data for inspection in HDF5 viewer ----
    import os
    from pathlib import Path
    spy.save(data, container = os.path.join(Path.home(), "spy_test"))



if __name__ == "__main__":
    #perform_freq_analysis()
    #dataset_arithmetic_and_preprocessing()
    connectivity_analysis()


# %%
