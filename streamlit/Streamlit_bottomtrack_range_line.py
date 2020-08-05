import streamlit as st
from rti_python_plot.plotly.plotly_bottomtrack_range_line import PlotlyBottomTrackRangeLine


class StreamlitBottomTrackRangeLine:
    """
    Create a streamlit Bottom Track Range line plot.
    This will get a plotly plot and use streamlit to display the data.
    """

    def __init__(self):
        self.plotly_bt_range = PlotlyBottomTrackRangeLine()

    def add_ens(self, ens):
        """
        Accumulate the Bottom Track data
        :param ens: Ensemble data to accumulate.
        """
        self.plotly_bt_range.add_ens(ens)

    def get_plot(self):
        """
        Get the Plotly Voltage Line Plot.
        """
        # Load the data from the file
        plot_title = "Bottom Track Range"

        fig, data = self.plotly_bt_range.get_plot()

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(data)

        # Create a streamlit plot
        st.plotly_chart(fig)

    @staticmethod
    def get_sqlite_plot(db_file_path: str):
        """
        Use streamlit to plot the plotly plot for the Bottom Track Range.
        :param db_file_path: File path to the sqlite db file.
        """
        # Get an SQLite plotly data
        fig, df_bt_range = PlotlyBottomTrackRangeLine().get_sqlite_plot(db_file_path)

        # Load the data from the file
        plot_title = "Bottom Track Range"

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_bt_range)

        # Create a streamlit plot
        st.plotly_chart(fig)

