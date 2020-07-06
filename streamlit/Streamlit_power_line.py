from pandas import DataFrame
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Ensemble.Ensemble import Ensemble


class StreamlitPowerLine:

    def __init__(self):
        # Column for the dataframe
        self.df_columns = ["dt", "type", "ss_code", "ss_config", "bin_num", "beam", "blank", "bin_size", "val"]
        # Use the load_data. notation to use variable within inner function
        self.df_all_data = DataFrame({}, columns=self.df_columns)

    def add_ens(self, ens):
        """
        Accumulate the Voltage data
        """

        # Get the data from the SystemSetup
        if ens.IsAncillaryData and ens.IsEnsembleData and ens.IsSystemSetup:
            # Get the information about the ensemble
            dt = ens.EnsembleData.datetime()
            ss_config = ens.EnsembleData.SubsystemConfig
            ss_code = ens.EnsembleData.SysFirmwareSubsystemCode

            # Get the dataframe with the voltage data
            df_ss = ens.SystemSetup.encode_df(dt, ss_code, ss_config)

            # Merge the data to the global dataframe buffer
            if self.df_all_data.empty:
                self.df_all_data = df_ss
            else:
                self.df_all_data = pd.concat([self.df_all_data, df_ss])

    def get_plot(self):
        """
        Get the Plotly Voltage Line Plot.
        """
        # Load the data from the file
        plot_title = "Voltage"

        # Get all the voltage data
        data = self.df_all_data.loc[self.df_all_data['type'] == Ensemble.CSV_VOLTAGE]

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(data)

        # Get the data to plot
        dates = data['dt']
        vals = data['val']

        # Create the Bottom Track Range Line
        line_plot = go.Scatter(
            x=dates,
            y=vals
        )

        # Combine all the plots
        plots = [line_plot]

        # Create the figure
        fig = go.Figure(data=plots)

        # Set the plot titles
        fig.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="Volts"
        )

        # Create a streamlit plot
        st.plotly_chart(fig)
