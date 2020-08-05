from pandas import DataFrame
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Ensemble.Ensemble import Ensemble
import sqlite3
from rti_python_plot.plotly.plotly_ancillary_line import PlotlyAncillaryLine


class StreamlitAncillaryLine:
    """
    Create a streamlit plot of the ancillary data.  This will take data live or
    from an sqlite file.
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

        # Set the options for the plot
        self.plotly_ancillary = PlotlyAncillaryLine(plot_heading=plot_heading,
                                                    plot_pitch=plot_pitch,
                                                    plot_roll=plot_roll,
                                                    plot_water_temp=plot_water_temp,
                                                    plot_sys_temp=plot_sys_temp,
                                                    plot_pressure=plot_pressure,
                                                    plot_xdcr_depth=plot_xdcr_depth,
                                                    plot_sos=plot_sos)

    def add_ens(self, ens):
        """
        Accumulate the ensemble Ancillary data
        :param ens: Ensemble data to accumulate.
        """
        self.plotly_ancillary.add_ens(ens)

    def get_plot_hpr(self):
        """
        Get the Plotly Voltage Line Plot.
        """
        # Load the data from the file
        plot_title = "Heading Pitch Roll"

        # Get the data from the accumulate plot
        fig_hpr, df_hpr = self.plotly_ancillary.get_plot_hpr()

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_hpr)

        # Create a streamlit plot
        st.plotly_chart(fig_hpr)

    @staticmethod
    def get_sqlite_plot(db_file_path: str):
        """
        Get the plots from the sqlite database file.
        :param db_file_path: Path to sqlite database file.
        """
        # Get an SQLite data plot
        plot_title = "Heading/Pitch/Roll"
        fig_hpr, df_hpr = PlotlyAncillaryLine().get_sqlite_plot_hpr(db_file_path, plot_title)

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_hpr)

        # Create a streamlit plot
        st.plotly_chart(fig_hpr)

        ################################
        # Get an SQLite data plot
        plot_title = "Water Temp/Speed of Sound"
        fig_sos, df_sos = PlotlyAncillaryLine().get_sqlite_plot_sos_watertemp(db_file_path, plot_title)

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_sos)

        # Create a streamlit plot
        st.plotly_chart(fig_sos)

        ################################
        # Get an SQLite data plot
        plot_title = "Water Temp/System Temp"
        fig_temp, df_temp = PlotlyAncillaryLine().get_sqlite_plot_temp(db_file_path, plot_title)

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_temp)

        # Create a streamlit plot
        st.plotly_chart(fig_temp)

        plot_title = "Depth/Pressure"
        fig_pressure, df_pressure = PlotlyAncillaryLine().get_sqlite_plot_pressure(db_file_path, plot_title)

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_pressure)

        # Create a streamlit plot
        st.plotly_chart(fig_pressure)

