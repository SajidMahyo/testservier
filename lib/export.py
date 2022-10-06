import json



def writeOutputJson(output, outputPath):
    with open(outputPath, 'w', encoding='utf8') as json_file:
        json.dump(output, json_file, ensure_ascii=False, indent=2)
