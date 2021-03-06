from pandas import DataFrame
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import datetime


class StreamlitMagDirLine:

    def __init__(self):
        self.df_earth_columns = ["dt", "type", "ss_code", "ss_config", "bin_num", "beam", "blank", "bin_size", "val"]
        # Use the load_data. notation to use variable within inner function
        self.ens_count = 0
        self.df_all_earth = DataFrame({}, columns=self.df_earth_columns)

        # Remove Ship Speed
        self.prev_bt_east = 0.0
        self.prev_bt_north = 0.0
        self.prev_bt_vertical = 0.0

        self.is_upward_looking = False

        # Bin Selector
        self.selected_bins = None

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

            # Create Dataframe
            if ens.IsAncillaryData and ens.IsEnsembleData:
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
        Get the Water Velocity Magnitude data from the global dataframe.
        """
        return self.df_all_earth.loc[self.df_all_earth['type'] == "Direction"]

    def get_bin_selector(self, min_bin:int=0, max_bin:int=200):
        self.selected_bins = st.multiselect(
            "Choose Bin Numbers", list(range(min_bin, max_bin)), [4]
        )
        if not self.selected_bins:
            st.error("Please select at least one bin.")

        return self.selected_bins

    def get_plot(self, plot_type:str="mag"):
        """
        Get the Plotly Magnitude Line Plot.
        :param plot_type: "mag" will plot magnitude data.  "dir" will plot direction data.
        """
        # Load the data from the file
        if plot_type == "dir":
            data = self.get_dir_data()
            plot_title = "Water Direction"
        else:
            data = self.get_mag_data()
            plot_title = "Water Velocity Magnitude"

        # data = data.loc[data["bin_num"] == selected_bins[0]]

        st.subheader("Raw Data")
        st.write(data)

        st.subheader(plot_title)

        sel_bin_data = data.loc[data["bin_num"] == self.selected_bins[0]]
        #min_data = sel_bin_data.drop(columns=["type", "ss_code", "ss_config", "beam", "bin_num", "dt"])

        dates = sel_bin_data['dt']
        vals = sel_bin_data['val']

        # Create the Bottom Track Range Line
        line_plot = go.Scatter(
            x=dates,
            y=vals
        )

        plots = [line_plot]

        fig = go.Figure(data=plots)

        st.plotly_chart(fig)

        #st.line_chart(min_data)