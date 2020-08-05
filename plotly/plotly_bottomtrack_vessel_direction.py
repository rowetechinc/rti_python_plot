from pandas import DataFrame
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Ensemble.Ensemble import Ensemble
import sqlite3


class PlotlyBottomTrackVesselDirectionLine:
    """
    Create a plotly figure for a Bottom Track Vessel Direction (Direction) line.
    You can feed it ensemble data or it can get the data from an
    sqlite database file.
    """


    @staticmethod
    def get_sqlite_plot(db_file_path: str, filter: bool = True, filter_max: float = 360):
        """
        Given the sqlite database, pull out all the data and plot it to fig.  Then return the figure
        and the dataframe of all the data plotted.
        :param db_file_path: File path to the sqlite db file.
        :param filter: Flag if the data should be filtered.
        :param filter_max: Maximum value to look for.  Default value is BAD_VELOCITY 88.88
        :return Plotly figure and dataframe of all data plotted.
        """
        # Get an SQLite connection
        conn = sqlite3.connect(db_file_path)

        # Query and get a dataframe result
        query_str = "SELECT dateTime, bottomtrack.vesselDirection from bottomtrack INNER JOIN ensembles ON bottomtrack.ensIndex=ensembles.id;"
        df_bt_dir = pd.read_sql_query(query_str, conn)
        # Close SQLite connection
        conn.close()

        # Filter data
        # Check if any of the values are BAD_VELOCITY.
        if filter:
            df_bt_dir['vesselDirection'] = df_bt_dir['vesselDirection'].apply(lambda x: x if not Ensemble.is_bad_velocity(x) else None)

        # Load the data from the file
        if filter:
            plot_title = "Bottom Track Vessel Direction (Filter Max: " + str(filter_max) + ")"
        else:
            plot_title = "Bottom Track Vessel Direction"

        # Create the Bottom Track Speed Line
        line_plot = go.Scatter(
            x=df_bt_dir['dateTime'],
            y=df_bt_dir['vesselDirection'],
            name="Vessel Direction"
        )

        # Combine all the plots
        plots = [line_plot]

        # Create the figure
        fig = go.Figure(data=plots)

        # Set the plot titles
        fig.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="Bottom Track Vessel Direction (degrees)"
        )

        return fig, df_bt_dir