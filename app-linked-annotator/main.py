import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

import os
import hover
from local_lib import create_embedded_dataset
from hover.core.explorer import BokehCorpusExplorer, BokehCorpusAnnotator
from hover.recipe.subroutine import link_size_and_range, link_selection
from bokeh.io import curdoc
from bokeh.layouts import row

dataset = create_embedded_dataset("model_template")

corpus_explorer = BokehCorpusExplorer(
    {"raw": dataset.dfs["raw"]},
    title="Explorer: use the search widget for highlights, then explore and select",
)

corpus_annotator = BokehCorpusAnnotator(
    {"raw": dataset.dfs["raw"]}, title="Annotator: apply labels to the selected points"
)

corpus_explorer.plot()
corpus_annotator.plot()

link_size_and_range(corpus_explorer.figure, corpus_annotator.figure)
link_selection(corpus_explorer.sources["raw"], corpus_annotator.sources["raw"])

curdoc().add_root(row(*[_plot.view() for _plot in [corpus_explorer, corpus_annotator]]))
curdoc().title = "Annotator-Plus"
