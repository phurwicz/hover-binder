import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

from local_lib import create_embedded_dataset, load_vectorizer
from hover.recipes.experimental import active_learning
from hover.core.neural import create_vector_net_from_module, VectorNet
from bokeh.io import curdoc

TASK_MODULE = "model_template"

# create a hover.core.SupervisableDataset
dataset = create_embedded_dataset(TASK_MODULE)

# load a vectorizer-neuralnet architecture for active learning
vectorizer = load_vectorizer(TASK_MODULE)


def vecnet_callback():
    model = create_vector_net_from_module(VectorNet, TASK_MODULE, dataset.classes)
    return model


# create and render bokeh document
doc = curdoc()
active_learning(dataset, vectorizer, vecnet_callback, width=800)(doc)
