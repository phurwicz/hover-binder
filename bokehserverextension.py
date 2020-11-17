from subprocess import Popen


def load_jupyter_server_extension(nbapp):
    """serve the bokeh-app directory with bokeh server"""
    Popen(["bokeh", "serve", "simple-annotator", "--port=8890", "--allow-websocket-origin=*"])
    #Popen(["bokeh", "serve", "linked-annotator", "--port=8891", "--allow-websocket-origin=*"])
