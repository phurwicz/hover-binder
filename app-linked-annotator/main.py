import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

from local_lib import create_embedded_dataset
from hover.recipes import linked_annotator
from bokeh.io import curdoc

# create a hover.core.SupervisableDataset
dataset = create_embedded_dataset("model_template").copy()

# create and render bokeh document
doc = curdoc()
linked_annotator(dataset, width=800)(doc)
