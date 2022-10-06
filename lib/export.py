import json


def writeOutputJson(output, outputPath):
    """Takes a dictionnary and a path to write it as a JSON file"""
    with open(outputPath, 'w', encoding='utf8') as json_file:
        json.dump(output, json_file, ensure_ascii=False, indent=2)
