import os
from urllib.parse import urljoin, urlparse


def binder_proxy_app_url(app_path, port=5006):
    """
    ???+ note "Find the URL of Bokeh server app in the current Binder session."

        Intended for visiting a Binder-hosted Bokeh server app.

        Will NOT work outside of Binder.
    """

    service_url_path = os.environ.get(
        "JUPYTERHUB_SERVICE_PREFIX", "/user/hover-binder/"
    )
    proxy_url_path = f"proxy/{port}/{app_path}"

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
