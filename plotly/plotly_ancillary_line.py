from pandas import DataFrame
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Ensemble.Ensemble import Ensemble
import sqlite3


class PlotlyAncillaryLine:
    """
    Create a Plotly plot from the Ancillary data.
    This will pull all the data from the ensemble data.  The ensemble data
    will be given live or through an sqlite database file.
    """

    def __init__(self,
                 plot_heading: bool = True,
                 plot_pitch: bool = True,
                 plot_roll: bool = True,
                 plot_water_temp: bool = True,
                 plot_sys_temp: bool = True,
                 plot_pressure: bool = True,
                 plot_xdcr_depth: bool = True,
                 plot_sos: bool = True):

        # Column for the dataframe
        self.df_columns = ["dt", "type", "ss_code", "ss_config", "bin_num", "beam", "blank", "bin_size", "val"]

        # Determine which plots to include
        self.plot_heading = plot_heading
        self.plot_pitch = plot_pitch
        self.plot_roll = plot_roll
        self.plot_water_temp = plot_water_temp
        self.plot_sys_temp = plot_sys_temp
        self.plot_pressure = plot_pressure
        self.plot_xdcr_depth = plot_xdcr_depth
        self.sos = plot_sos

        # Create a buffer for all the ensemble data
        self.df_all_data = DataFrame({}, columns=self.df_columns)

    def add_ens(self, ens):
        """
        Accumulate the ensemble Ancillary data
        """

        # Get the data from the SystemSetup
        if ens.IsAncillaryData and ens.IsEnsembleData:
            # Get the information about the ensemble
            dt = ens.EnsembleData.datetime()
            ss_config = ens.EnsembleData.SubsystemConfig
            ss_code = ens.EnsembleData.SysFirmwareSubsystemCode

            # Get the dataframe with the voltage data
            df_anc = ens.AncillaryData.encode_df(dt, ss_code, ss_config)

            # Merge the data to the global dataframe buffer
            if self.df_all_data.empty:
                self.df_all_data = df_anc
            else:
                self.df_all_data = pd.concat([self.df_all_data, df_anc])

    def get_plot_hpr(self):
        """
        Get the Plotly Voltage Line Plot.
        """
        # Load the data from the file
        plot_title = "Heading Pitch Roll"

        # Get all the voltage data
        df_hpr = self.df_all_data.loc[(self.df_all_data['type'] == Ensemble.CSV_HEADING) | (self.df_all_data['type'] == Ensemble.CSV_PITCH) | (self.df_all_data['type'] == Ensemble.CSV_ROLL)]
        df_heading = self.df_all_data.loc[self.df_all_data['type'] == Ensemble.CSV_HEADING]
        df_pitch = self.df_all_data.loc[self.df_all_data['type'] == Ensemble.CSV_PITCH]
        df_roll = self.df_all_data.loc[self.df_all_data['type'] == Ensemble.CSV_ROLL]

        # Create each line plot
        line_heading = go.Scatter(x=df_heading['dt'], y=df_heading['val'], mode='lines', name='Heading')
        line_pitch = go.Scatter(x=df_pitch['dt'], y=df_pitch['val'], mode='lines', name='Pitch')
        line_roll = go.Scatter(x=df_roll['dt'], y=df_roll['val'], mode='lines', name='Roll')

        # Create the figure
        fig_hpr = go.Figure()
        fig_hpr.add_trace(line_heading)
        fig_hpr.add_trace(line_pitch)
        fig_hpr.add_trace(line_roll)

        # Set the plot titles
        fig_hpr.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="Degrees"
        )

        return fig_hpr, df_hpr

    @staticmethod
    def get_sqlite_plot_hpr(db_file_path: str, plot_title: str):
        """
        Create the plot for heading pitch and roll and get the data.
        :param db_file_path: SQLite database file path.
        :param plot_title: Plot title.
        """
        # Get an SQLite connection
        conn = sqlite3.connect(db_file_path)

        # Query and get a dataframe result
        df_hpr = pd.read_sql_query("SELECT dateTime, heading, pitch, roll from ensembles; ", conn)

        # Close SQLite connection
        conn.close()

        # Create line plots
        line_heading = go.Scatter(x=df_hpr['dateTime'], y=df_hpr['heading'], mode='lines', name='Heading')
        line_pitch = go.Scatter(x=df_hpr['dateTime'], y=df_hpr['pitch'], mode='lines', name='Pitch')
        line_roll = go.Scatter(x=df_hpr['dateTime'], y=df_hpr['roll'], mode='lines', name='Roll')

        # Create the figure
        fig_hpr = go.Figure()
        fig_hpr.add_trace(line_heading)
        fig_hpr.add_trace(line_pitch)
        fig_hpr.add_trace(line_roll)

        # Set the plot titles
        fig_hpr.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="Degrees"
        )

        return fig_hpr, df_hpr

    @staticmethod
    def get_sqlite_plot_sos_watertemp(db_file_path: str, plot_title: str):
        """
        Create the plot for Speed of Sound and Water Temp and get the data.
        :param db_file_path: SQLite database file path.
        :param plot_title: Plot title.
        """
        # Get an SQLite connection
        conn = sqlite3.connect(db_file_path)

        # Query and get a dataframe result
        df = pd.read_sql_query("SELECT dateTime, waterTemp, sos from ensembles; ", conn)

        # Close SQLite connection
        conn.close()

        # Create line plots
        line_heading = go.Scatter(x=df['dateTime'], y=df['waterTemp'], mode='lines', name='Water Temp')
        line_pitch = go.Scatter(x=df['dateTime'], y=df['sos'], mode='lines', name='Speed of Sound')

        # Create the figure
        fig = go.Figure()
        fig.add_trace(line_heading)
        fig.add_trace(line_pitch)

        # Set the plot titles
        fig.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="C"
        )

        return fig, df

    @staticmethod
    def get_sqlite_plot_temp(db_file_path: str, plot_title: str):
        """
        Create the plot for Speed of Sound and Water Temp and get the data.
        :param db_file_path: SQLite database file path.
        :param plot_title: Plot title.
        """
        # Get an SQLite connection
        conn = sqlite3.connect(db_file_path)

        # Query and get a dataframe result
        df = pd.read_sql_query("SELECT dateTime, waterTemp, sysTemp from ensembles; ", conn)

        # Close SQLite connection
        conn.close()

        # Create line plots
        line_heading = go.Scatter(x=df['dateTime'], y=df['waterTemp'], mode='lines', name='Water Temp')
        line_pitch = go.Scatter(x=df['dateTime'], y=df['sysTemp'], mode='lines', name='System Temp')

        # Create the figure
        fig = go.Figure()
        fig.add_trace(line_heading)
        fig.add_trace(line_pitch)

        # Set the plot titles
        fig.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="C"
        )

        return fig, df

    @staticmethod
    def get_sqlite_plot_pressure(db_file_path: str, plot_title: str):
        """
        Create the plot for Speed of Sound and Water Temp and get the data.
        :param db_file_path: SQLite database file path.
        :param plot_title: Plot title.
        """
        # Get an SQLite connection
        conn = sqlite3.connect(db_file_path)

        # Query and get a dataframe result
        df = pd.read_sql_query("SELECT dateTime, pressure, xdcrDepth from ensembles; ", conn)

        # Close SQLite connection
        conn.close()

        # Create line plots
        line_depth = go.Scatter(x=df['dateTime'], y=df['xdcrDepth'], mode='lines', name='System Temp')

        # Create the figure
        fig = go.Figure()
        fig.add_trace(line_depth)

        # Set the plot titles
        fig.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="m"
        )

        return fig, df