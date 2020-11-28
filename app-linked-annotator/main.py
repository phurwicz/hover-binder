import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

import os
import hover
from local_lib import create_embedded_dataset
from hover.core.explorer import BokehCorpusExplorer, BokehCorpusAnnotator
from bokeh.io import curdoc
from bokeh.layouts import row

dataset = create_embedded_dataset("model_template")

corpus_explorer = BokehCorpusExplorer(
    {"raw": dataset.dfs["raw"]},
    title="Explorer: use the search widget for highlights, then explore and select",
    height=600,
    width=600,
)

corpus_annotator = BokehCorpusAnnotator(
    {"raw": dataset.dfs["raw"]},
    title="Annotator: apply labels to the selected points",
    height=600,
    width=600,
)

corpus_explorer.plot()
corpus_annotator.plot()

corpus_explorer.link_xy_range(corpus_annotator)
corpus_explorer.link_selection("raw", corpus_annotator, "raw")

curdoc().add_root(row(*[_plot.view() for _plot in [corpus_explorer, corpus_annotator]]))
curdoc().title = "Linked-Annotator"
