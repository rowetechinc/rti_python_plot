from pandas import DataFrame
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Ensemble.Ensemble import Ensemble
import sqlite3


class PlotlyBottomTrackRangeLine:
    """
    Create a plotly figure for a Bottom Track Range line.
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
        if ens.IsAncillaryData and ens.IsEnsembleData and ens.IsBottomTrack:
            # Get the information about the ensemble
            dt = ens.EnsembleData.datetime()
            ss_config = ens.EnsembleData.SubsystemConfig
            ss_code = ens.EnsembleData.SysFirmwareSubsystemCode

            # Get the dataframe with the voltage data
            df_ss = ens.BottomTrack.encode_df(dt, ss_code, ss_config)

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
        data = self.df_all_data.loc[self.df_all_data['type'] == Ensemble.CSV_BT_RANGE]

        # Get the data to plot
        dates = data['dt']
        vals = data['val']

        # Create the Bottom Track Range Line
        b0_line_plot = go.Scatter(
            x=dates,
            y=vals.loc[data['beam'] == 0],
            name='Beam0'
        )

        # Create the Bottom Track Range Line
        b1_line_plot = go.Scatter(
            x=dates,
            y=vals.loc[data['beam'] == 1],
            name='Beam1'
        )

        # Create the Bottom Track Range Line
        b2_line_plot = go.Scatter(
            x=dates,
            y=vals.loc[data['beam'] == 2],
            name='Beam2'
        )

        # Create the Bottom Track Range Line
        b3_line_plot = go.Scatter(
            x=dates,
            y=vals.loc[data['beam'] == 3],
            name='Beam3'
        )

        # Combine all the plots
        plots = [b0_line_plot, b1_line_plot, b2_line_plot, b3_line_plot]

        # Create the figure
        fig = go.Figure(data=plots)

        # Set the plot titles
        fig.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="Bottom Track Range"
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
        query_str = "SELECT dateTime, bottomtrack.rangeBeam0, bottomtrack.rangeBeam1, bottomtrack.rangeBeam2, bottomtrack.rangeBeam3  from bottomtrack INNER JOIN ensembles ON bottomtrack.ensIndex=ensembles.id;"
        df_bt_range = pd.read_sql_query(query_str, conn)
        # Close SQLite connection
        conn.close()

        # Load the data from the file
        plot_title = "Bottom Track Range"

        # Create the Bottom Track Range Beam 0 Line
        b0_line_plot = go.Scatter(
            x=df_bt_range['dateTime'],
            y=df_bt_range['rangeBeam0'],
            name="Range Beam 0"
        )

        # Create the Bottom Track Range Beam 1 Line
        b1_line_plot = go.Scatter(
            x=df_bt_range['dateTime'],
            y=df_bt_range['rangeBeam1'],
            name="Range Beam 1"
        )

        # Create the Bottom Track Range Beam 2 Line
        b2_line_plot = go.Scatter(
            x=df_bt_range['dateTime'],
            y=df_bt_range['rangeBeam2'],
            name="Range Beam 2"
        )

        # Create the Bottom Track Range Beam 3 Line
        b3_line_plot = go.Scatter(
            x=df_bt_range['dateTime'],
            y=df_bt_range['rangeBeam3'],
            name="Range Beam 3"
        )

        # Combine all the plots
        plots = [b0_line_plot, b1_line_plot, b2_line_plot, b3_line_plot]

        # Create the figure
        fig = go.Figure(data=plots)

        # Set the plot titles
        fig.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="Range (m)",
            yaxis=dict(autorange='reversed'),
        )

        return fig, df_bt_range