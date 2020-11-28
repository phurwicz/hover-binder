import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

import os
import hover
from local_lib import create_embedded_dataset
from hover.core.explorer import BokehCorpusAnnotator
from bokeh.io import curdoc
from bokeh.layouts import row

dataset = create_embedded_dataset("model_template")

corpus_annotator = BokehCorpusAnnotator(
    {"raw": dataset.dfs["raw"]},
    title="Annotator: apply labels to the selected points",
    height=600,
    width=600,
)

corpus_annotator.plot()

curdoc().add_root(row(corpus_annotator.view()))
curdoc().title = "Simple-Annotator"
