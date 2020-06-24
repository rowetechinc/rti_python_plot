from bokeh.server.server import Server
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from tornado.ioloop import IOLoop
from threading import Thread
from rti_python_plot.bokeh.rti_bokeh_plot_manager import RtiBokehPlotManager


class RtiBokehServer:

    def __init__(self, rti_config, plot_manager=None):

        self.rti_config = rti_config

        # Bokeh App
        # Created when the server is created
        self.bokeh_app = None

        # Create the plot manager
        # This handles all the incoming data and pass it to the plots
        if plot_manager:
            self.plot_manager = plot_manager
        else:
            self.plot_manager = RtiBokehPlotManager(rti_config)
            self.plot_manager.start()

        # Create an app object by setting the path of the bokeh plot in the webserver
        # and setting the function to call to create a plot webpage
        apps = {'/': self.get_bokeh_app()}


        # Create the Bokeh server with the given port and IP address
        # The configuration has the local IP address.  If you share the config
        # file, you must delete the IP line so the configuration will regenerate the
        # configuration file with a new IP line which is the local computers IP address
        bokeh_port = int(self.rti_config.config['PLOT']['PORT'])
        bokeh_ip = self.rti_config.config['PLOT']['IP']
        websocket_allow = bokeh_ip + ":" + str(bokeh_port)
        self.server = Server(apps, port=bokeh_port, address=bokeh_ip, allow_websocket_origin=[websocket_allow])
        self.server.start()

        # Only display the webpage if enabled
        if self.rti_config.config.getboolean('PLOT', 'LIVE'):
            self.server.show('/')

        # Outside the notebook ioloop needs to be started
        # Start the loop in a thread so it does not block
        loop = IOLoop.current()
        #loop.start()
        t = Thread(target=loop.start, daemon=True)
        t.start()

    def get_bokeh_app(self):
        """
        Generate a single instance of the bokeh app.

        The plot manager handles all the data to the plots.
        :return: Bokeh app created.
        """
        if self.bokeh_app is None:
            handler = FunctionHandler(self.plot_manager.setup_bokeh_server)
            self.bokeh_app = Application(handler)

        return self.bokeh_app
