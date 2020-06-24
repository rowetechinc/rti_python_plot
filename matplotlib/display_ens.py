from typing import Tuple
from rti_python.Ensemble.Ensemble import Ensemble
import numpy as np
import matplotlib.pyplot as plt

class DisplayEnsembles():

    def __init__(self):

        self.num_bin = 30
        self.num_beam = 4

        self.ss_setup = dict()        # NumBins,NumBeam

        self.amp_0 = dict()
        self.avg_amp = dict()
        self.min_amp_0 = dict()
        self.max_amp_0 = dict()

    def process_ens(self, ens: Ensemble):
        """
        Process the ensemble.  Get all the Ensemble data.
        :param ens: Ensemble data.
        :return:
        """

        # Get the subsystem config
        ss_config = self.get_ss_id(ens)

        # Get the number of bins and beams
        (num_bin, num_beam) = self.get_setup(ens)
        self.ss_setup[ss_config] = (num_bin, num_beam)

        # Process the Amplitude data
        self.process_amp(ens, ss_config)

    def get_setup(self, ens: Ensemble) -> Tuple[int, int]:
        """
        Get the number of beams and bin.
        :param ens: Ensemble data.
        :return: num_bins, num_beams
        """
        num_bins = 0
        num_beams = 0

        if ens.IsEnsembleData:
            num_bins = ens.EnsembleData.NumBins
            num_beams = ens.EnsembleData.NumBeams

        return (num_bins, num_beams)

    def get_ss_id(self, ens: Ensemble) -> str:
        """
        Get the Subsystem config and code to generate a custom id for each subsystem config.
        :param ens: Ensemble data.
        :return: ssCode_ssConfig
        """
        ss_code = "0"
        ss_config = "0"

        # Get the subsystem code and config
        if ens.IsEnsembleData:
            ss_code = ens.EnsembleData.SysFirmwareSubsystemCode
            ss_config = str(ens.EnsembleData.SubsystemConfig)

        return ss_code + "_" + ss_config

    def process_amp(self, ens: Ensemble, ss_config: str):
        """
        Get the amplitude data.  Calculate the average, min and max.
        :param ens: Ensemble data.
        :return:
        """

        if ens.IsAmplitude:
            if ens.Amplitude.element_multiplier > 0:
                beam0 = [row[0] for row in ens.Amplitude.Amplitude]
                beam0 = np.asarray(beam0, 'float')
                beam0 = DisplayEnsembles.replace_bad_vel_with_nan(beam0)

                # Add data to list in dictionary
                if ss_config not in self.amp_0:
                    self.amp_0[ss_config] = []          # Create a list

                self.amp_0[ss_config].append(beam0)
                plt.plot(beam0)
                plt.pause(0.05)
                plt.show(block=False)

                # Calculate Max and add to dictionary
                if ss_config in self.max_amp_0:
                    beam0_max = DisplayEnsembles.max_values(beam0, self.max_amp_0[ss_config])
                    self.max_amp_0[ss_config] = beam0_max
                else:
                    self.max_amp_0[ss_config] = beam0

            if ens.Amplitude.element_multiplier > 1:
                beam1 = [row[1] for row in ens.Amplitude.Amplitude]
                beam1 = np.asarray(beam1, 'float')
                beam1 = DisplayEnsembles.replace_bad_vel_with_nan(beam1)
            if ens.Amplitude.element_multiplier > 2:
                beam2 = [row[2] for row in ens.Amplitude.Amplitude]
                beam2 = np.asarray(beam2, 'float')
                beam2 = DisplayEnsembles.replace_bad_vel_with_nan(beam2)
            if ens.Amplitude.element_multiplier > 3:
                beam3 = [row[3] for row in ens.Amplitude.Amplitude]
                beam3 = np.asarray(beam3, 'float')
                beam3 = DisplayEnsembles.replace_bad_vel_with_nan(beam3)

    def plot_amp_min_max_avg(self):
        #for val in self.max_amp_0.values():
            #plt.scatter(val)

        plt.show()

    @staticmethod
    def replace_bad_vel_with_nan(values: []) -> []:
        values = values.astype('float')
        #values[Ensemble.is_float_close(values, Ensemble.BadVelocity)] = np.nan
        values[values == Ensemble.BadVelocity] = np.nan  # or use np.nan
        return values

    @staticmethod
    def max_values(new_values: [], max_values: []) -> []:
        return np.maximum(new_values, max_values)