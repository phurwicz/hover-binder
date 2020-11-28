# Hover Example Apps

### (works out-of-the-box on Binder)

This repository demonstrates the usage of [hover](https://github.com/phurwicz/hover) to understand and supervise a machine learning task.

## Simple Annotator [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/phurwicz/hover-binder/master?urlpath=/proxy/5006/app-simple-annotator)

- use the lasso/tap/poly tool to select data points
- assign your labels and hit "Apply"
- in a real use case on your computer, "Export" will save a DataFrame
- take advantage of the text/regex search box

## Linked Annotator [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/phurwicz/hover-binder/master?urlpath=/proxy/5006/app-linked-annotator)

![Demo](images/app-linked-annotator.gif)

- on top of the `Simple Annotator`, showes another plot which is focused on search
- the search boxes are independent across plots, minimizing interference in between
- :bulb: the selections in the plots are synchronized. You can select in one and label in the other!

## Snorkel Annotator [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/phurwicz/hover-binder/master?urlpath=/proxy/5006/app-snorkel-annotator)

- compared with the `Linked Annotator`, replaces the left plot with Snorkel labeling function outputs
- in a real use case, you can check the labeling functions and your annotations against each other.
- :bulb: one could also exploit labeling functions as sophisticated "filters" to help find interesting data points!
