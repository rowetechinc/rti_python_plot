from pandas import DataFrame
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Ensemble.Ensemble import Ensemble
import sqlite3


class PlotlyBottomTrackBeamVelocityLine:
    """
    Create a plotly figure for a Bottom Track Beam Velocity line.
    You can feed it ensemble data or it can get the data from an
    sqlite database file.
    """


    @staticmethod
    def get_sqlite_plot(db_file_path: str, filter: bool = True, filter_max: float = 88.8):
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
        query_str = "SELECT dateTime, bottomtrack.beamVelBeam0, bottomtrack.beamVelBeam1, bottomtrack.beamVelBeam2, bottomtrack.beamVelBeam3  from bottomtrack INNER JOIN ensembles ON bottomtrack.ensIndex=ensembles.id;"
        df_bt_range = pd.read_sql_query(query_str, conn)
        # Close SQLite connection
        conn.close()

        # Filter data
        # Check if any of the values exceed the filter_max.
        # Use the absolute value to compare against
        if filter:
            df_bt_range['beamVelBeam0'] = df_bt_range['beamVelBeam0'].apply(lambda x: x if x and abs(x) <= filter_max else None)
            df_bt_range['beamVelBeam1'] = df_bt_range['beamVelBeam1'].apply(lambda x: x if x and abs(x) <= filter_max else None)
            df_bt_range['beamVelBeam2'] = df_bt_range['beamVelBeam2'].apply(lambda x: x if x and abs(x) <= filter_max else None)
            df_bt_range['beamVelBeam3'] = df_bt_range['beamVelBeam3'].apply(lambda x: x if x and abs(x) <= filter_max else None)

        # Load the data from the file
        if filter:
            plot_title = "Bottom Track Beam Velocity (Filter Max: " + str(filter_max) + ")"
        else:
            plot_title = "Bottom Track Beam Velocity"

        # Create the Bottom Track Beam Velocity Beam 0 Line
        b0_line_plot = go.Scatter(
            x=df_bt_range['dateTime'],
            y=df_bt_range['beamVelBeam0'],
            name="Beam Vel Beam 0"
        )

        # Create the Bottom Track Beam Velocity Beam 1 Line
        b1_line_plot = go.Scatter(
            x=df_bt_range['dateTime'],
            y=df_bt_range['beamVelBeam1'],
            name="Beam Vel Beam 1"
        )

        # Create the Bottom Track Beam Velocity Beam 2 Line
        b2_line_plot = go.Scatter(
            x=df_bt_range['dateTime'],
            y=df_bt_range['beamVelBeam2'],
            name="Beam Vel Beam 2"
        )

        # Create the Bottom Track Beam Velocity Beam 3 Line
        b3_line_plot = go.Scatter(
            x=df_bt_range['dateTime'],
            y=df_bt_range['beamVelBeam3'],
            name="Beam Vel Beam 3"
        )

        # Combine all the plots
        plots = [b0_line_plot, b1_line_plot, b2_line_plot, b3_line_plot]

        # Create the figure
        fig = go.Figure(data=plots)

        # Set the plot titles
        fig.update_layout(
            title=plot_title,
            xaxis_title="DateTime",
            yaxis_title="Bottom Track Beam Velocity (m/s)"
        )

        return fig, df_bt_range