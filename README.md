# Running a bokeh server with Binder

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/phurwicz/hover-binder/master?urlpath=/proxy/8890/simple-annotator) Simple Annotator
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/phurwicz/hover-binder/master?urlpath=/proxy/8891/linked-annotator) Linked Annotator


This repository demonstrates the usage of [hover](https://github.com/phurwicz/hover) to understand and supervise a machine learning task.


## Instructions from @binder-examples/bokeh

1. Created a `bokeh-app` directory in the repo with a `main.py` file in it. This is the application that will be served. We've added the
   [Bokeh weather example](https://github.com/bokeh/bokeh/tree/master/examples/app/weather) as a demo. 
2. Installed `bokeh` for the viz and `jupyter_server_proxy` which we'll use to direct people to the port on which Bokeh runs. See `environment.yml`.
3. Added a custom server extension (`bokehserverextension.py`) that will be run to direct people to the Bokeh app (which is run on a port)
4. Used `postBuild` to enable the `jupyter_server_proxy` extension, then set up and enable our custom server extension for Bokeh. 
5. Created a Binder link that uses `urlpath` to point users to the port on which the Bokeh server will run:

   ```
   https://mybinder.org/v2/gh/binder-examples/bokeh/master?urlpath=/proxy/5006/bokeh-app
   ```
   
When people click on the Binder link, they should be directed to the running Bokeh app.
