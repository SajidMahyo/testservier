import pandas as pd
import numpy as np


from utils.loading import (
    load
)






clinical_trials = load("data/clinical_trials.csv", "schema/clinical_trials.yaml")
drugs = load("data/drugs.csv", "schema/drugs.yaml")
pubmed = pd.concat([load("data/pubmed.csv", "schema/pubmed.yaml"), load("data/pubmed.json", "schema/pubmed.yaml")])



# print(clinical_trials)
# print(drugs)
# print(pubmed)





