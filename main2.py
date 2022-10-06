import json
from collections import Counter

#Read the graph
with open("output/link_graph.json", 'r') as f:
    graph = json.load(f)

#Extract the full journal list from all drugs (and remove the duplicate for the same drug)
journalList = list()
for drug, elem in graph.items():
    journalList.extend(set(d['journal'] for d in elem['references']['journals']))


#Print the number drug referenced by each journal and order them by most_common
print(Counter(journalList).most_common())

# Result
# -> [('Journal of emergency nursing', 2), ('Psychopharmacology', 2), ('The journal of maternal-fetal & neonatal medicine', 2), ('The Journal of pediatrics', 1), ('Journal of food protection', 1), ('American journal of veterinary research', 1), ('The journal of allergy and clinical immunology. In practice', 1), ('Journal of photochemistry and photobiology. B, Biology', 1), ('Journal of back and musculoskeletal rehabilitation', 1), ('Hôpitaux Universitaires de Genève', 1)]
# Looks like 'Journal of emergency nursing', 'Psychopharmacology' and 'The journal of maternal-fetal & neonatal medicine' are eaven with 2 drugs referenced.