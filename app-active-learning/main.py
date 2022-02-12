import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

from local_lib import create_embedded_dataset, load_vectorizer
from hover.recipes.experimental import active_learning
from hover.core.neural import VectorNet
from hover.utils.common_nn import LogisticRegression
from bokeh.io import curdoc

TASK_MODULE = "model_template"

# create a hover.core.SupervisableDataset
dataset = create_embedded_dataset(TASK_MODULE).copy()

vecnet = VectorNet(vectorizer, LogisticRegression, "model.pt", dataset.classes)

# create and render bokeh document
doc = curdoc()
active_learning(dataset, vecnet, width=800)(doc)
