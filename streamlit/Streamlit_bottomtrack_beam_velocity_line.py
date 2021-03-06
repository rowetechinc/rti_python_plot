import streamlit as st
from rti_python_plot.plotly.plotly_bottomtrack_beam_vel_line import PlotlyBottomTrackBeamVelocityLine


class StreamlitBottomTrackBeamVelocityLine:
    """
    Create a streamlit Bottom Track Beam Velocity line plot.
    This will get a plotly plot and use streamlit to display the data.
    """

    @staticmethod
    def get_sqlite_plot(db_file_path: str, filter: bool = True, filter_max: float = 88.8):
        """
        Use streamlit to plot the plotly plot for the Bottom Track Beam Velocity.
        :param db_file_path: File path to the sqlite db file.
        :param filter: Flag if the data should be filtered.
        :param filter_max: Maximum value to look for.  Default value is BAD_VELOCITY 88.88
        """
        # Get an SQLite plotly data
        fig, df_bt_range = PlotlyBottomTrackBeamVelocityLine().get_sqlite_plot(db_file_path, filter=filter, filter_max=filter_max)

        # Load the data from the file
        if filter:
            plot_title = "Bottom Track Beam Velocity (Filter Max: " + str(filter_max) + ")"
        else:
            plot_title = "Bottom Track Beam Velocity"

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_bt_range)

        # Create a streamlit plot
        st.plotly_chart(fig)

