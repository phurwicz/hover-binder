import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

import os
import hover
from local_lib import create_embedded_dataset, link_plots
from hover.core.explorer import BokehCorpusExplorer, BokehCorpusAnnotator
from bokeh.io import curdoc
from bokeh.layouts import row

dataset = create_embedded_dataset("model_template")

corpus_explorer = BokehCorpusExplorer(dataset.dfs["raw"], title="Explorer: use the search widget for highlights, then explore and select")
corpus_annotator = BokehCorpusAnnotator(dataset.dfs["raw"], title="Annotator: apply labels to the selected points")

linked_plots = link_plots(corpus_explorer, corpus_annotator)

curdoc().add_root(row(*[_plot.view() for _plot in linked_plots]))
curdoc().title = "Annotator-Plus"
