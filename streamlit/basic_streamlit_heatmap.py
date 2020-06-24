from rti_python.Utilities.read_binary_file import ReadBinaryFile
from pandas import DataFrame
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import datetime
from rti_python.Utilities.check_binary_file import RtiCheckFile


df_earth_columns = ["dt", "type", "ss_code", "ss_config", "bin_num", "beam", "blank", "bin_size", "val"]
st.title("RTI Test Streamlit")

@st.cache
def load_data():
    # Use the load_data. notation to use variable within inner function
    load_data.ens_count = 0
    load_data.df_all_earth = DataFrame({}, columns=df_earth_columns)

    # Remove Ship Speed
    load_data.prev_bt_east = 0.0
    load_data.prev_bt_north = 0.0
    load_data.prev_bt_vertical = 0.0

    def process_ens_func(sender, ens):
        """
        Receive the data from the file.  It will process the file.
        When an ensemble is found, it will call this function with the
        complete ensemble.
        :param ens: Ensemble to process.
        :return:
        """
        if ens.EarthVelocity:
            # Remove Ship speed
            ens.EarthVelocity.remove_vessel_speed(load_data.prev_bt_east,
                                                  load_data.prev_bt_north,
                                                  load_data.prev_bt_vertical)

            # Keep track of previous BT speed
            if ens.IsBottomTrack and ens.BottomTrack.NumBeams >= 3:
                load_data.prev_bt_east = ens.BottomTrack.EarthVelocity[0]
                load_data.prev_bt_north = ens.BottomTrack.EarthVelocity[1]
                load_data.prev_bt_vertical = ens.BottomTrack.EarthVelocity[2]

            # Create Dataframe
            if ens.IsAncillaryData and ens.IsEnsembleData:
                df_earth = ens.EarthVelocity.encode_df(ens.EnsembleData.datetime(),
                                                       ens.EnsembleData.SysFirmwareSubsystemCode,
                                                       ens.EnsembleData.SubsystemConfig,
                                                       0.0,                                 # Replace BadVelocity
                                                       0.0,                                 # Replace BadVelocity
                                                       False,                               # Do not include bad velocity
                                                       False)                               # Do not include bad velocity

                load_data.ens_count = load_data.ens_count + 1

                # Convert to dataframe
                #df_earth = DataFrame(dict_earth, columns=df_earth_columns)

                # Merge the data to the global buffer
                if load_data.df_all_earth.empty:
                    load_data.df_all_earth = df_earth
                else:
                    #df_all_earth.append(df_earth, ignore_index=True, sort=False)
                    load_data.df_all_earth = pd.concat([load_data.df_all_earth, df_earth])



    # Create the file reader to read the binary file
    #ead_binary = ReadBinaryFile()
    #read_binary.ensemble_event += process_ens_func
    rti_check = RtiCheckFile()
    rti_check.ensemble_event += process_ens_func
    rti_check.select_and_process()

    # Just define the file path
    #file_path = r"C:\Users\rico\Documents\Adcp1.ens"

    # Pass the file path to the reader
    #read_binary.playback(file_path)

    print(load_data.df_all_earth)
    print(str(load_data.ens_count))

    return load_data.df_all_earth.loc[load_data.df_all_earth['type'] == "Magnitude"]


# Gives the user notice that data is loading
data_load_state = st.text("Loading data...")

# Load the data from the file
data = load_data()

# Tell user, loading is complete
data_load_state.text("Loading data...done!")

selected_bins = st.multiselect(
    "Choose Bin Numbers", list(range(0, 29)), [4]
)
if not selected_bins:
    st.error("Please select at least one bin.")

#data = data.loc[data["bin_num"] == selected_bins[0]]

st.subheader("Raw Data")
st.write(data)

st.subheader("Plot Magnitude")

sel_bin_data = data.loc[data["bin_num"] == selected_bins[0]]
min_data = sel_bin_data.drop(columns=["type", "ss_code", "ss_config", "beam", "bin_num", "dt"])

st.line_chart(min_data)

st.subheader("Heatmap")
programmers = data['bin_num']
dates = data['dt']
z = data['val']

st.write(data)

fig = go.Figure(data=go.Heatmap(
        z=z,
        x=dates,
        y=programmers,
        colorscale='Viridis'))

fig.update_layout(
    title="Velocity Magnitude",
    xaxis_title="DateTime",
    yaxis_title="Bin Number",
    yaxis_autorange='reversed'         # Downward looking 'reversed'
)



st.plotly_chart(fig)
