import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

import os
import hover
from local_lib import create_embedded_dataset
from hover.core.explorer import BokehSnorkelExplorer, BokehCorpusAnnotator
from hover.recipe.subroutine import link_size_and_range, link_selection
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.models import Button
from bokeh.events import ButtonClick
import snorkel_template
from snorkel_template import LABELING_FUNCTIONS
from importlib import reload

dataset = create_embedded_dataset("model_template")

snorkel_explorer = BokehSnorkelExplorer(
    {"raw": dataset.dfs["raw"], "labeled": dataset.dfs["dev"]},
    title="Snorkel: square for correct, x for incorrect, + for missed; click on legends to hide or show LF",
)

corpus_annotator = BokehCorpusAnnotator(
    {"raw": dataset.dfs["raw"]}, title="Annotator: apply labels to the selected points"
)

snorkel_explorer.plot()
corpus_annotator.plot()
for _lf in LABELING_FUNCTIONS:
    snorkel_explorer.plot_lf(_lf)
snorkel_explorer.figure.legend.click_policy = "hide"

link_size_and_range(snorkel_explorer.figure, corpus_annotator.figure)
link_selection(snorkel_explorer.sources["raw"], corpus_annotator.sources["raw"])

# lf_reloader = Button(label="Reload LF", button_type="primary")
#
# def reload_lf():
#    """
#    Callback function.
#    """
#    reload(snorkel_template)
#    from snorkel_template import LABELING_FUNCTIONS
#    snorkel_explorer.reset_figure()
#    snorkel_explorer.plot()
#    for _lf in LABELING_FUNCTIONS:
#        snorkel_explorer.plot_lf(_lf)
#
# lf_reloader.on_event(ButtonClick, reload_lf)

# curdoc().add_root(row(lf_reloader, *[_plot.view() for _plot in [snorkel_explorer, corpus_annotator]]))
curdoc().add_root(
    row(*[_plot.view() for _plot in [snorkel_explorer, corpus_annotator]])
)
curdoc().title = "Snorkel-Annotator"
