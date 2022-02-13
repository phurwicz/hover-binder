import os
import json
import warnings
import subprocess
from functools import lru_cache
from urllib.parse import urljoin, urlparse


def jupyter_port_to_token(port=None, jupyterlab=False):
    """
    ???+ note "Find the token of a local Jupyter server."
    """
    jupyter_key = "lab" if jupyterlab else "notebook"
    process = subprocess.run(
        ["jupyter", jupyter_key, "list", "--json"],
        capture_output=True,
        check=True,
        timeout=10,
    )
    pieces = process.stdout.decode("utf-8").split("\n")
    for _piece in pieces:
        try:
            _dict = json.loads(_piece)
            _port = _dict["port"]
            if _port == port or port is None:
                return _dict["token"]
        except Exception as e:
            warnings.warn(f"Caught an error: {e}")
    return None


def binder_proxy_app_url(app_path, port=5006, jupyter_port=8888, jupyterlab=False):
    """
    ???+ note "Find the URL of Bokeh server app in the current Binder session."

        Intended for visiting a Binder-hosted Bokeh server app.

        Will NOT work outside of Binder.
    """

    service_url_path = os.environ.get(
        "JUPYTERHUB_SERVICE_PREFIX", "/user/hover-binder/"
    )
    token = jupyter_port_to_token(port=jupyter_port, jupyterlab=jupyterlab)
    proxy_url_path = f"proxy/{port}/{app_path}?token={token}"

    base_url = "https://hub.gke2.mybinder.org"
    user_url_path = urljoin(service_url_path, proxy_url_path)
    full_url = urljoin(base_url, user_url_path)
    return full_url


def remote_jupyter_proxy_url(port):
    """
    ???+ note "Callable to configure Bokeh's show method when using a proxy (JupyterHub)."

        Intended for rendering a in-notebook Bokeh app.

        Usage:

        ```python
        # show(plot)
        show(plot, notebook_url=remote_jupyter_proxy_url)
        ```
    """

    # find JupyterHub base (external) url, default to Binder
    base_url = os.environ.get("JUPYTERHUB_BASE_URL", "https://hub.gke2.mybinder.org")
    host = urlparse(base_url).netloc

    if port is None:
        return host

    service_url_path = os.environ.get(
        "JUPYTERHUB_SERVICE_PREFIX", "/user/hover-binder/"
    )
    proxy_url_path = f"proxy/{port}"

    user_url = urljoin(base_url, service_url_path)
    full_url = urljoin(user_url, proxy_url_path)
    return full_url
