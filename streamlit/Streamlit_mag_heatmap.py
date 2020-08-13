import streamlit as st
from rti_python_plot.plotly.plotly_heatmap_mag import PlotlyHeatmapMag


class StreamlitMagHeatmap:
    """
    Create a streamlit Magnitude Heatmap plot.
    This will get a plotly plot and use streamlit to display the data.
    """

    def __init__(self):
        self.plotly_hm = PlotlyHeatmapMag()

    def add_ens(self, ens):
        """
        Accumulate the Voltage data
        :param ens: Ensemble data to accumulate.
        """
        self.plotly_hm.add_ens(ens)

    def get_plot(self):
        """
        Get the Plotly Voltage Line Plot.
        """
        # Load the data from the file
        plot_title = "Voltage"

        fig, data = self.plotly_hm.get_plot()

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(data)

        # Create a streamlit plot
        st.plotly_chart(fig)

    @staticmethod
    def get_sqlite_plot(db_file_path: str):
        """
        Use streamlit to plot the plotly plot for the power.
        :param db_file_path: File path to the sqlite db file.
        """
        # Get an SQLite plotly data
        fig, df_hm = PlotlyHeatmapMag().get_sqlite_plot(db_file_path)

        # Load the data from the file
        plot_title = "Water Magnitude"

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_hm)

        # Create a streamlit plot
        st.plotly_chart(fig)

