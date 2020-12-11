import os
import wrappy
import hover
from hover.utils.datasets import newsgroups_dictl
from hover.core.dataset import SupervisableTextDataset


# define functions that provide crucial intermediates
@wrappy.memoize(cache_limit=10)
def load_vectorizer(module_name):
    from importlib import import_module

    module = import_module(module_name)
    return module.get_vectorizer()


@wrappy.memoize(cache_limit=10, return_copy=False)
def create_embedded_dataset(module_name):
    data_home = os.path.join(os.path.dirname(__file__), "../scikit_learn_data/")
    my_20ng, label_encoder, label_decoder = newsgroups_dictl(data_home=data_home)

    # taking a small subset of the data so that the Binder example loads faster
    split_idx = int(0.1 * len(my_20ng["train"]))
    # split_idx = int(0.9 * len(my_20ng["train"]))
    dataset = SupervisableTextDataset(
        raw_dictl=my_20ng["train"][:split_idx],
        dev_dictl=my_20ng["train"][split_idx : int(split_idx * 1.2)],
        # dev_dictl=my_20ng["train"][split_idx:],
        test_dictl=my_20ng["test"],
    )

    vectorizer = load_vectorizer(module_name)
    dataset.compute_2d_embedding(vectorizer, "umap")
    dataset.synchronize_df_to_dictl()

    return dataset
