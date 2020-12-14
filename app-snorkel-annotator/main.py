import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

import hover
from local_lib import create_embedded_dataset
from hover.recipes.experimental import snorkel_crosscheck
from bokeh.io import curdoc
from snorkel_template import LABELING_FUNCTIONS

# create a hover.core.SupervisableDataset
dataset = create_embedded_dataset("model_template").copy()


# create and render bokeh document
doc = curdoc()
snorkel_crosscheck(dataset, LABELING_FUNCTIONS, width=800)(doc)
