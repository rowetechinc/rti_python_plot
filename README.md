# Installation
Install the required libraries.

```commandline
pip install -r requirements.txt
```

# Reading in Data From File

```python
from rti_python.Utilities.check_binary_file import RtiCheckFile

rti_check = RtiCheckFile()
rti_check.ensemble_event += self.ens_handler
rti_check.select_and_process()

def ens_handler(self, sender, ens):
    #if ens.IsEnsembleData:
    #    print(str(ens.EnsembleData.EnsembleNumber))
```

# Bokeh Plots

```python
from rti_python_plot.bokeh.rti_bokeh_plot_data import RtiBokehPlotData
from rti_python_plot.bokeh.rti_bokeh_plot_manager import RtiBokehPlotManager
from rti_python_plot.bokeh.rti_bokeh_server import RtiBokehServer
        
self.rti_config = RtiConfig()
self.rti_config.init_average_waves_config()
self.rti_config.init_terminal_config()
self.rti_config.init_waves_config()
self.rti_config.init_plot_server_config()from rti_python.Utilities.config import RtiConfig

self.plot_manager = RtiBokehPlotManager(self.rti_config)
self.plot_manager.start()
self.bokeh_server = RtiBokehServer(self.rti_config, self.plot_manager)

def ens_handler(self, sender, ens):
    #if ens.IsEnsembleData:
    #    print(str(ens.EnsembleData.EnsembleNumber))

    self.plot_manager.update_dashboard_ens(ens)
```

# Streamlit
The python file must be run through streamlit to start the streamlit server
```commandline
streamlit run app.py
```

Streamlit then looks for any streamlit data and will display it in the web browser.
Load all the data first, then display all the streamlit information.

## Test a file out
Clone rti_python is same project


```commandline
streamlit run streamlit run rti_python_plot\streamlit\basic_streamlit_heatmap.py
```

```python
from rti_python_plot.streamlit.streamlit_heatmap import StreamlitHeatmap
from rti_python_plot.streamlit.streamlit_mag_dir_line import StreamlitMagDirLine

self.heatmap = StreamlitHeatmap()
self.mag_dir_line = StreamlitMagDirLine()

# Load data
rti_check = RtiCheckFile()
rti_check.ensemble_event += self.ens_handler
rti_check.select_and_process()

# Then display data
# Plot heatmap
self.heatmap.get_plot("mag")
self.heatmap.get_plot("dir")

# Plot mag and direction line plot
self.mag_dir_line.get_bin_selector()
self.mag_dir_line.get_plot("mag")
self.mag_dir_line.get_plot("dir")

def ens_handler(self, sender, ens):
    # Add data to heatmap
    self.heatmap.add_ens(ens)
    self.mag_dir_line.add_ens(ens)
```



# MATPLOTLIB usage

```python
from rti_python_plot.matplotlib.display_ens import DisplayEnsembles

self.display_ens = DisplayEnsembles()

def ens_handler(self, sender, ens):
    #if ens.IsEnsembleData:
    #    print(str(ens.EnsembleData.EnsembleNumber))

    self.display_ens.process_ens(ens)
```

