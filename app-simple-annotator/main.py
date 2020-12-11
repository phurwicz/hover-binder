import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

from local_lib import create_embedded_dataset
from hover.recipes.experimental import simple_annotator
from bokeh.io import curdoc

# create a hover.core.SupervisableDataset
dataset = create_embedded_dataset("model_template").copy()

# tell bokeh to create a document
doc = curdoc()

# render the document
simple_annotator(dataset)(doc)
