import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

from local_lib import create_embedded_dataset, load_vectorizer

import hover
from hover.core.explorer import BokehSoftLabelExplorer, BokehCorpusAnnotator
from hover.core.neural import create_vector_net_from_module, VectorNet
from hover.module_config import ABSTAIN_DECODED as ABSTAIN

from bokeh.io import curdoc
from bokeh.layouts import row, column
from bokeh.models import Button, Slider
from bokeh.models import ColumnDataSource, DataTable, TableColumn
from wasabi import msg as logger
import pandas as pd

TASK_MODULE = "model_template"
SIDEBAR_WIDTH = 300

dataset = create_embedded_dataset(TASK_MODULE)
vectorizer = load_vectorizer(TASK_MODULE)

for _key in ["raw", "dev"]:
    dataset.dfs[_key]["pred_label"] = ABSTAIN
    dataset.dfs[_key]["pred_score"] = 0.5

softlabel_explorer = BokehSoftLabelExplorer(
    {"raw": dataset.dfs["raw"], "labeled": dataset.dfs["dev"]},
    "pred_label",
    "pred_score",
    title="Prediction Visualizer: retrain model and locate confusions",
    height=600,
    width=600,
)

corpus_annotator = BokehCorpusAnnotator(
    {"raw": dataset.dfs["raw"]},
    title="Annotator: apply labels to the selected points",
    height=600,
    width=600,
)

softlabel_explorer.plot()
corpus_annotator.plot()

softlabel_explorer.link_xy_range(corpus_annotator)
softlabel_explorer.link_selection("raw", corpus_annotator, "raw")


def setup_model_retrainer():
    model_retrainer = Button(
        label="Train model", button_type="primary", width=SIDEBAR_WIDTH
    )
    epochs_slider = Slider(
        start=1, end=20, value=1, step=1, title="# epochs", width=SIDEBAR_WIDTH
    )

    def retrain_model():
        """
        Callback function.
        """
        dataset.setup_label_coding()
        model = create_vector_net_from_module(VectorNet, TASK_MODULE, dataset.classes)

        train_loader = dataset.loader("raw", vectorizer, smoothing_coeff=0.2)
        dev_loader = dataset.loader("dev", vectorizer)

        _ = model.train(train_loader, dev_loader, epochs=epochs_slider.value)
        logger.good("Callback 1/2: retrained model")

        for _key in ["raw", "dev"]:
            _probs = model.predict_proba(dataset.dfs[_key]["text"].tolist())
            _labels = [dataset.label_decoder[_val] for _val in _probs.argmax(axis=-1)]
            _scores = _probs.max(axis=-1).tolist()
            dataset.dfs[_key]["pred_label"] = pd.Series(_labels)
            dataset.dfs[_key]["pred_score"] = pd.Series(_scores)

        softlabel_explorer._update_sources()
        softlabel_explorer.plot()
        logger.good("Callback 2/2: updated predictions")

    model_retrainer.on_click(retrain_model)
    return model_retrainer, epochs_slider


def setup_pop_updater():
    pop_updater = Button(
        label="Update population", button_type="primary", width=SIDEBAR_WIDTH
    )
    population_source = ColumnDataSource(dict())
    population_columns = [
        TableColumn(field="label", title="label", width=150),
        TableColumn(field="count_raw", title="raw", width=50),
        TableColumn(field="count_dev", title="dev", width=50),
    ]
    population_table = DataTable(
        source=population_source,
        columns=population_columns,
        width=SIDEBAR_WIDTH,
        height=SIDEBAR_WIDTH * 3,
        fit_columns=False,
        index_width=50,
    )

    def update_population():
        """
        Callback function.
        """
        pop_raw = dataset.dfs["raw"]["label"].value_counts()
        pop_dev = dataset.dfs["dev"]["label"].value_counts()

        labels = sorted(dataset.classes)
        count_raw = [pop_raw.get(_label, 0) for _label in labels]
        count_dev = [pop_dev.get(_label, 0) for _label in labels]
        data = dict(label=labels, count_raw=count_raw, count_dev=count_dev)
        population_source.data = data
        logger.good("Callback: updated population")

    update_population()
    pop_updater.on_click(update_population)
    return pop_updater, population_table


model_retrainer, epochs_slider = setup_model_retrainer()
pop_updater, population_table = setup_pop_updater()

sidebar = column(model_retrainer, epochs_slider, pop_updater, population_table)

curdoc().add_root(
    row(sidebar, *[_plot.view() for _plot in [softlabel_explorer, corpus_annotator]])
)
curdoc().title = "Active-Learning"
