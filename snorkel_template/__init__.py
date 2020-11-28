from hover.utils.snorkel_helper import labeling_function
from hover import module_config
import re


@labeling_function(targets=["rec.autos"])
def auto_keywords(row):
    flag = re.search(r"(wheel|diesel|gasoline|automobile|vehicle)", row.text)
    return "rec.autos" if flag else module_config.ABSTAIN_DECODED


@labeling_function(targets=["rec.sport.baseball"])
def baseball_keywords(row):
    flag = re.search(r"(baseball|stadium|\ bat\ |\ base\ )", row.text)
    return "rec.sport.baseball" if flag else module_config.ABSTAIN_DECODED


@labeling_function(targets=["sci.crypt"])
def crypt_keywords(row):
    flag = re.search(r"(crypt|math|encode|decode|key)", row.text)
    return "sci.crypt" if flag else module_config.ABSTAIN_DECODED


@labeling_function(targets=["talk.politics.guns"])
def guns_keywords(row):
    flag = re.search(r"(gun|rifle|ammunition|violence|shoot)", row.text)
    return "talk.politics.guns" if flag else module_config.ABSTAIN_DECODED


@labeling_function(targets=["misc.forsale"])
def forsale_keywords(row):
    flag = re.search(r"(sale|deal|price|discount)", row.text)
    return "misc.forsale" if flag else module_config.ABSTAIN_DECODED


LABELING_FUNCTIONS = [
    auto_keywords,
    baseball_keywords,
    crypt_keywords,
    guns_keywords,
    forsale_keywords,
]
