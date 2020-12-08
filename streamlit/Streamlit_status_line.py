import streamlit as st
from rti_python_plot.plotly.plotly_status_line import PlotlyStatusLine


class StreamlitStatusLine:
    """
    Create a streamlit Status line plot.
    This will get a plotly plot and use streamlit to display the data.
    """

    def __init__(self):
        self.plotly_status = PlotlyStatusLine()

    def add_ens(self, ens):
        """
        Accumulate the Voltage data
        :param ens: Ensemble data to accumulate.
        """
        self.plotly_status.add_ens(ens)

    def get_plot(self):
        """
        Get the Plotly Voltage Line Plot.
        """
        # Load the data from the file
        plot_title = "Status"

        fig, data = self.plotly_status.get_plot()

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
        fig, df_status = PlotlyStatusLine().get_sqlite_plot(db_file_path)

        # Load the data from the file
        plot_title = "Status"

        # Create a Header
        st.subheader(plot_title)

        # Display a table of the data
        st.write(df_status)

        # Create a streamlit plot
        st.plotly_chart(fig)

