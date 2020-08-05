from pandas import DataFrame
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import datetime


class StreamlitHeatmap:

    def __init__(self):
        self.df_earth_columns = ["dt", "type", "ss_code", "ss_config", "bin_num", "beam", "blank", "bin_size", "val"]
        # Use the load_data. notation to use variable within inner function
        self.ens_count = 0
        self.df_all_earth = DataFrame({}, columns=self.df_earth_columns)

        # Remove Ship Speed
        self.prev_bt_east = 0.0
        self.prev_bt_north = 0.0
        self.prev_bt_vertical = 0.0

        self.bin_size = 0.0
        self.blank = 0

        self.is_upward_looking = False

    def add_ens(self, ens):
        """
        Receive the data from the file.  It will process the file.
        When an ensemble is found, it will call this function with the
        complete ensemble.
        :param self:
        :param ens: Ensemble to process.
        :return:
        """
        if ens.EarthVelocity:
            # Remove Ship speed
            ens.EarthVelocity.remove_vessel_speed(self.prev_bt_east,
                                                  self.prev_bt_north,
                                                  self.prev_bt_vertical)

            # Keep track of previous BT speed
            if ens.IsBottomTrack and ens.BottomTrack.NumBeams >= 3:
                self.prev_bt_east = ens.BottomTrack.EarthVelocity[0]
                self.prev_bt_north = ens.BottomTrack.EarthVelocity[1]
                self.prev_bt_vertical = ens.BottomTrack.EarthVelocity[2]
                df_bt = ens.BottomTrack.encode_df(ens.EnsembleData.datetime(),
                                                       ens.EnsembleData.SysFirmwareSubsystemCode,
                                                       ens.EnsembleData.SubsystemConfig)

                # Merge the data to the global buffer
                if self.df_all_earth.empty:
                    self.df_all_earth = df_bt
                else:
                    #df_all_earth.append(df_earth, ignore_index=True, sort=False)
                    self.df_all_earth = pd.concat([self.df_all_earth, df_bt])

            # Create Dataframe
            if ens.IsAncillaryData and ens.IsEnsembleData:
                self.blank = ens.AncillaryData.FirstBinRange
                self.bin_size = ens.AncillaryData.BinSize

                df_earth = ens.EarthVelocity.encode_df(ens.EnsembleData.datetime(),
                                                       ens.EnsembleData.SysFirmwareSubsystemCode,
                                                       ens.EnsembleData.SubsystemConfig,
                                                       0.0,                                 # Replace BadVelocity
                                                       0.0,                                 # Replace BadVelocity
                                                       False,                               # Do not include bad velocity
                                                       False)                               # Do not include bad velocity

                # Check if upward or downward looking
                self.is_upward_looking = ens.AncillaryData.is_upward_facing()

                self.ens_count = self.ens_count + 1

                # Convert to dataframe
                #df_earth = DataFrame(dict_earth, columns=df_earth_columns)

                # Merge the data to the global buffer
                if self.df_all_earth.empty:
                    self.df_all_earth = df_earth
                else:
                    #df_all_earth.append(df_earth, ignore_index=True, sort=False)
                    self.df_all_earth = pd.concat([self.df_all_earth, df_earth])

    @st.cache
    def get_mag_data(self):
        """
        Get the Water Velocity Magnitude data from the global dataframe.
        """
        return self.df_all_earth.loc[self.df_all_earth['type'] == "Magnitude"]

    @st.cache
    def get_dir_data(self):
        """
        Get the Water Direction data from the global dataframe.
        """
        return self.df_all_earth.loc[self.df_all_earth['type'] == "Direction"]

    @st.cache
    def get_avg_range_data(self):
        """
        Get the Average Range data from the global dataframe.
        """
        return self.df_all_earth.loc[self.df_all_earth['type'] == "BT_Avg_Range"]

    def get_plot(self, plot_type: str = "mag"):
        """
        Get the Plotly Magnitude Heatmap.
        :param plot_type: "mag" will plot magnitude data.  "dir" will plot direction data.
        """
        # Load the data from the file
        if plot_type == "dir":
            data = self.get_dir_data()
            plot_title = "Water Direction"
        else:
            data = self.get_mag_data()
            plot_title = "Water Velocity Magnitude"

        # Get the bottom range values
        bt_range = self.get_avg_range_data()

        st.subheader("Heatmap")
        bin_nums = data['bin_num']
        bin_depth = (data['bin_num'] * self.bin_size) + self.blank
        dates = data['dt']
        z = data['val']

        st.write(data)
        st.write(bt_range)
        #st.write(bin_nums)
        #st.write(bin_depth)

        # Create the heatmap
        heatmap = go.Heatmap(
            z=z,
            x=dates,
            y=bin_depth,
            colorscale='Cividis')  # Viridis, Inferno, Cividis, RdBu, Bluered_r, ["red", "green", "blue"]), [(0, "red"), (0.5, "green"), (1, "blue")]

        # Create the Bottom Track Range Line
        bt_line = go.Scatter(
            x=bt_range['dt'],
            y=bt_range['val']
        )

        plots = [heatmap, bt_line]

        fig = go.Figure(data=plots)

        if self.is_upward_looking:
            fig.update_layout(
                title=plot_title,
                xaxis_title="DateTime",
                yaxis_title="Bin Number"
            )
        else:
            fig.update_layout(
                title=plot_title,
                xaxis_title="DateTime",
                yaxis_title="Bin Number",
                yaxis_autorange='reversed'  # Downward looking 'reversed'
            )

        st.plotly_chart(fig)