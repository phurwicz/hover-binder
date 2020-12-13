import os
import wrappy
import hover
from hover.utils.datasets import newsgroups_dictl
from hover.core.dataset import SupervisableTextDataset
from hover.module_config import ABSTAIN_DECODED

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

    split_idx = int(0.9 * len(my_20ng["train"]))
    # taking smaller sample so that the example loads faster
    dataset = SupervisableTextDataset(
        raw_dictl=my_20ng["train"][: int(split_idx * 0.9)][:2000],
        train_dictl=my_20ng["train"][int(split_idx * 0.9) : split_idx],
        dev_dictl=my_20ng["train"][split_idx:][:500],
        # test_dictl=my_20ng["test"][:1000],
    )
    dataset.dfs["raw"]["label"] = ABSTAIN_DECODED

    vectorizer = load_vectorizer(module_name)
    dataset.compute_2d_embedding(vectorizer, "umap")
    dataset.synchronize_df_to_dictl()

    return dataset
