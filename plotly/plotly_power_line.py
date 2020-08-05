from pandas import DataFrame
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Ensemble.Ensemble import Ensemble
import sqlite3


class PlotlyPowerLine:
    """
    Create a plotly figure for a Power line.
    You can feed it ensemble data or it can get the data from an
    sqlite database file.
    """

    def __init__(self):
        """
        Create the dataframe to store the data from the ensembles.
        """
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
        :return Plotly figure and a dataframe of the data used for the plot.
        """
        # Load the data from the file
        plot_title = "Voltage"

        # Get all the voltage data
        data = self.df_all_data.loc[self.df_all_data['type'] == Ensemble.CSV_VOLTAGE]

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

        return fig, data

    @staticmethod
    def get_sqlite_plot(db_file_path: str):
        """
        Given the sqlite database, pull out all the data and plot it to fig.  Then return the figure
        and the dataframe of all the data plotted.
        :param db_file_path: File path to the sqlite db file.
        :return Plotly figure and dataframe of all data plotted.
        """
        # Get an SQLite connection
        conn = sqlite3.connect(db_file_path)

        # Query and get a dataframe result
        df_volt = pd.read_sql_query("SELECT dateTime, Voltage from ensembles; ", conn)

        # Close SQLite connection
        conn.close()

        # Load the data from the file
        plot_title = "Voltage"

        # Create the Voltage Line
        line_plot = go.Scatter(
            x=df_volt['dateTime'],
            y=df_volt['Voltage']
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

        return fig, df_volt