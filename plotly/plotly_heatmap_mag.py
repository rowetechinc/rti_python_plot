from pandas import DataFrame
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Ensemble.Ensemble import Ensemble
import sqlite3
from collections import deque

class PlotlyHeatmapMag:
    """
    Create a plotly figure for a Magnitude Heatmap.
    You can feed it ensemble data or it can get the data from an
    sqlite database file.
    """

    def __init__(self):
        """
        Initialize the queues to hold all the ensemble data.
        The queues will contain all the accumulated information.
        """
        self.bad_velocity = Ensemble.BadVelocity

        #self.queue_mag = deque(maxlen=max_display_points)
        self.list_mag = []
        self.queue_dt = deque()
        self.queue_bin_depth = deque()
        self.queue_bt_dt = deque()
        self.queue_bt_range = deque()
        self.queue_bottom = deque()
        self.bin_depth_list = []
        self.blank = 0.0
        self.bin_size = 0.0
        self.is_upward_looking = False

    def get_sqlite_plot(self, db_file_path: str):
        """
        Get the data from the sqlite file.
        Then add it to the queue so it will be plotted on the next update.
        """
        # Create a connection to the sqlite file
        # Get an SQLite connection
        conn = sqlite3.connect(db_file_path)

        # Query and get a dataframe result
        df_volt = pd.read_sql_query("SELECT dateTime, Voltage from ensembles; ", conn)

        df_bt_range = pd.read_sql_query('SELECT ensembles.ensnum, ensembles.dateTime, ensembles.numbeams, ensembles.numbins, '
                                        'ensembles.binsize, ensembles.rangefirstbin, '
                                        'rangebeam0, rangebeam1, rangebeam2, rangebeam3, avgRange '
                                        'FROM ensembles '
                                        'INNER JOIN bottomtrack ON ensembles.id = bottomtrack.ensindex '
                                        'WHERE ensembles.project_id = 1 '
                                        'ORDER BY ensembles.ensnum ASC;', conn)

        df_mag = pd.read_sql_query('SELECT ensembles.dateTime, ensembles.subsystemCode, ensembles.SubsystemConfig, '
                                   'WpMagDir.bin, ensembles.rangeFirstBin, ensembles.binSize, ensembles.isUpwardLooking, WpMagDir.mag '
                                   'FROM ensembles '
                                   'INNER JOIN WpMagDir ON ensembles.id = WpMagDir.ensindex '
                                   'WHERE ensembles.project_id = 1 '
                                   'ORDER BY ensembles.dateTime ASC;', conn)

        # Close SQLite connection
        conn.close()

        # Find all the unique datetime to separate the ensembles
        # Then add them to the queue
        unique_dt = df_mag.dateTime.unique()
        self.queue_dt.extend(unique_dt)

        # Set the depth list
        # Get the first dt to get all the bins associated with a specific datetime (ensemble)
        first_dt = unique_dt.flat[0]
        first_ens = df_mag.loc[df_mag['dateTime'] == first_dt]
        self.is_upward_looking = bool(first_ens['isUpwardLooking'].iloc[0])
        self.bin_size = first_ens['binSize'].iloc[0]
        self.blank = first_ens['rangeFirstBin'].iloc[0]

        # Get all the unique bin numbers
        # Sort them to be in order
        unique_bin_num = df_mag.bin.unique()
        unique_bin_num.sort()

        for bin_num in unique_bin_num:
            # Add the bins depths to the list
            self.bin_depth_list.append(self.blank + (self.bin_size * bin_num))

            # Get all the values for each bin
            bin_mags = df_mag.loc[df_mag['bin'] == bin_num]

            # Remove any bad velocity data
            # Bad velocity is greater than 88.88
            # Convert to numpy array first then remove value
            bin_mags_np = np.array(bin_mags['mag'].tolist())
            bin_mags_list = np.where(bin_mags_np >= self.bad_velocity, None, bin_mags_np).tolist()

            # Add a deque to the list for each bin
            self.list_mag.append([])

            # Set all the magnitude values to the list
            self.list_mag[bin_num].extend(bin_mags_list)

        # Get all the range values for the bottom track line
        self.queue_bt_range.extend(df_bt_range['avgRange'].tolist())

        # Get the datetime for the bottom track values
        self.queue_bt_dt.extend(df_bt_range['dateTime'].tolist())

        # Create a line at the bottom of the plot to connect to the bottom track line
        # Make the length of the list the same as the number of range values
        self.queue_bottom.extend([max(self.bin_depth_list)]*len(df_bt_range['avgRange'].tolist()))

        # Convert the list of deque magnitudes to a list of magnitudes
        #mag_list = []
        #for mag_deque in self.list_mag:
        #    mag_list.append(list(mag_deque))

        # Load the data from the file
        plot_title = "Water Magnitude"

        # Create the Voltage Line
        bt_line = go.Scatter(
            x=list(self.queue_bt_dt),
            y=list(self.queue_bt_range),
            #name="Bottom Track Range (m)",
            showlegend=False,
            line=dict(color='rgba(255, 69, 0, 255)', width=2),
        )

        # Create the Voltage Line
        bottom_line = go.Scatter(
            x=list(self.queue_bt_dt),
            y=list(self.queue_bottom),
            fill='tonexty',
            showlegend=False,
            line=dict(color='rgba(105, 105, 105, 255)', width=10),
            fillcolor='rgba(105, 105, 105, 255)'
        )

        mag_data = go.Heatmap( z=self.list_mag,
                               x=list(self.queue_dt),
                               y=self.bin_depth_list,
                               hoverongaps=False,
                               name='Magnitude',
                               colorscale='Cividis')

        # Combine all the plots
        plots = [mag_data, bt_line, bottom_line]

        # Create the figure
        fig = go.Figure(data=plots)

        if self.is_upward_looking:
            # Set the plot titles
            fig.update_layout(
                title=plot_title,
                xaxis_title="DateTime",
                yaxis_title="Bin Depth (m)",
                #showlegend=True
            )
        else:
            # Set the plot titles
            fig.update_layout(
                title=plot_title,
                xaxis_title="DateTime",
                yaxis_title="Bin Depth (m)",
                yaxis=dict(autorange='reversed'),
                #showlegend=True
            )

        return fig, df_mag
