import pandas as pd
import numpy as np


from lib.loading import load
from lib.export import writeOutputJson









def formatDate(date):
    return date.strftime("%d, %B %Y") if not pd.isnull(date) else ""

def formatStr(elem):
    return str(elem) if not pd.isnull(elem) else ""

def main():
    #load the datasets from flat files
    clinical_trials = load("data/clinical_trials.csv", "schema/clinical_trials.yaml")
    drugs = load("data/drugs.csv", "schema/drugs.yaml")
    pubmed = pd.concat([load("data/pubmed.csv", "schema/pubmed.yaml"), load("data/pubmed.json", "schema/pubmed.yaml")])

    #initialize the output variable
    output = dict()

    for index, drug in drugs.iterrows():

        journalRef = list()
        pubmedRef = list()
        clinicalTrialsRef = list()

        for index, matchingPub in pubmed.loc[pubmed['title'].str.contains(drug["drug"], case=False)].iterrows():
            pubmedRef.append({'id' : formatStr(matchingPub['id']), 'title' : formatStr(matchingPub['title']), 'date' : formatDate(matchingPub['date']) })
            journalRef.append({'journal' : formatStr(matchingPub['journal']), 'date' : formatDate(matchingPub['date'])})

        for index, matchingTrial in clinical_trials.loc[clinical_trials['scientific_title'].str.contains(drug["drug"], case=False)].iterrows():
            clinicalTrialsRef.append({'title' : formatStr(matchingTrial['scientific_title']), 'date' : formatDate(matchingTrial['date'])})
            journalRef.append({'journal' : formatStr(matchingTrial['journal']), 'date' : formatDate(matchingTrial['date'])})


        output[drug["drug"]] = {'atccode' : drug["atccode"], 'references' : {'pubmed': pubmedRef, 'clinical_trials' : clinicalTrialsRef, 'journals' : journalRef}}
    writeOutputJson(output, "output/link_graph.json")


if __name__ == "__main__":
    main()



