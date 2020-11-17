import sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

import os
import hover
from hover.workflow import Automated
from hover.utils.public_dataset import newsgroups_dictl
from hover.future.core.dataset import SupervisableTextDataset
from hover.future.core.explorer import BokehCorpusExplorer, BokehCorpusAnnotator
from bokeh.io import curdoc
from bokeh.layouts import row


# define functions that provide crucial intermediates
def create_workflow():
    """
    For demonstrative purposes.
    """
    data_home = os.path.join(os.path.dirname(__file__), 'scikit_learn_data/')
    my_20ng, label_encoder, label_decoder = newsgroups_dictl(data_home=data_home)

    # taking a small subset of the data so that the Binder example loads faster
    split_idx = int(0.1 * len(my_20ng["train"]))
    #split_idx = int(0.9 * len(my_20ng["train"]))
    dataset = SupervisableTextDataset(
        raw_dictl=my_20ng["train"][:split_idx],
        dev_dictl=my_20ng["train"][split_idx:int(split_idx * 1.2)],
        #dev_dictl=my_20ng["train"][split_idx:],
        test_dictl=my_20ng["test"],
    )

    dataset.dfs["raw"].drop(["label"], inplace=True, axis=1)
    dataset.synchronize_df_to_dictl()

    workflow = Automated(dataset=dataset, model_module_name="model_template")
    workflow.compute_text_to_2d("umap")

    return workflow

def workflow_to_plots(workflow):
    corpus_explorer = BokehCorpusExplorer(
        workflow.dataset.dfs["raw"],
        title="Corpus Explorer",
    )
    corpus_annotator = BokehCorpusAnnotator(
        workflow.dataset.dfs["raw"],
        title="Corpus Annotator",
    )
    
    # pack together all the plots for display, then specify linking behaviors
    linked_plots = [
        corpus_explorer,
        corpus_annotator,
    ]
    
    for i, _pi in enumerate(linked_plots):
        _pi.figure.plot_height = 600
        _pi.figure.plot_width = 800
        for j, _pj in enumerate(linked_plots):
            if not i == j:
                # link coordinate ranges
                for _attr in ["start", "end"]:
                    _pi.figure.x_range.js_link(
                        _attr, _pj.figure.x_range, _attr,
                    )
                    _pi.figure.y_range.js_link(
                        _attr, _pj.figure.y_range, _attr,
                    )
                # link selection
                _pi.source.selected.js_link(
                    "indices", _pj.source.selected, "indices"
                )
                
    return linked_plots

workflow = create_workflow()
linked_plots = workflow_to_plots(workflow)
curdoc().add_root(row(*[_plot.view() for _plot in linked_plots]))
curdoc().title = "Annotator-Plus"