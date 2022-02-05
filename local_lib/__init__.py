"""
Utility module for common functions shared across demo apps.
"""
import os
import wrappy
from hover.utils.datasets import newsgroups_reduced_dictl, newsgroups_dictl
from hover.core.dataset import SupervisableTextDataset

# define functions that provide crucial intermediates
@wrappy.memoize(cache_limit=10)
def load_vectorizer(module_name):
    from importlib import import_module

    module = import_module(module_name)
    return module.get_vectorizer()


@wrappy.memoize(cache_limit=10, return_copy=False)
def create_embedded_dataset(module_name, reduced=True):
    data_home = os.path.join(os.path.dirname(__file__), "../scikit_learn_data/")
    if reduced:
        my_20ng, _, _ = newsgroups_reduced_dictl(data_home=data_home)
    else:
        my_20ng, _, _ = newsgroups_dictl(data_home=data_home)

    split_idx = int(0.9 * len(my_20ng["train"]))
    # taking smaller sample so that the example loads faster
    dataset = SupervisableTextDataset(
        # raw_dictl=my_20ng["train"][: int(split_idx * 0.9)],
        raw_dictl=my_20ng["train"][: int(split_idx * 0.9)][:2000],
        # train_dictl=my_20ng["train"][int(split_idx * 0.9) : split_idx],
        # dev_dictl=my_20ng["train"][split_idx:],
        train_dictl=my_20ng["train"][int(split_idx * 0.9) : split_idx],
        dev_dictl=my_20ng["train"][split_idx:][:500],
        # test_dictl=my_20ng["test"][:1000],
    )

    vectorizer = load_vectorizer(module_name)
    dataset.compute_2d_embedding(vectorizer, "umap")
    dataset.synchronize_df_to_dictl()

    return dataset
