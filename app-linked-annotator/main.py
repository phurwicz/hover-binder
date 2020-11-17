import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

import os
import hover
from local_lib import create_workflow, link_plots
from hover.future.core.explorer import BokehCorpusExplorer, BokehCorpusAnnotator
from bokeh.io import curdoc
from bokeh.layouts import row

workflow = create_workflow()

corpus_explorer = BokehCorpusExplorer(
    workflow.dataset.dfs["raw"],
    title="Corpus Explorer",
)
corpus_annotator = BokehCorpusAnnotator(
    workflow.dataset.dfs["raw"],
    title="Corpus Annotator",
)

linked_plots = link_plots(
    corpus_explorer,
    corpus_annotator,
)

curdoc().add_root(row(*[_plot.view() for _plot in linked_plots]))
curdoc().title = "Annotator-Plus"