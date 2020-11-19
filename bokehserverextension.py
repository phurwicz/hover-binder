from subprocess import Popen
import time


def load_jupyter_server_extension(nbapp):
    """serve the bokeh-app directory with bokeh server"""
    Popen([
        "bokeh",
        "serve",
        "app-simple-annotator",
        "app-linked-annotator",
        "--allow-websocket-origin=*",
    ])

    time.sleep(10)
    Popen([
        "curl",
        "http://localhost:5006/app-simple-annotator",
    ])

if __name__ == "__main__":
    load_jupyter_server_extension(None)
