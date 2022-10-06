import pandas as pd
import numpy as np
from datetime import datetime
import yaml
import json

from utils.errors import (
    SchemaNotMatchingData,
    UnknownType,
    NotHandledFileExtension
)

def toString(elem):
    """Take an element as input and return the string associated. Return np.nan if the element doesn't correspond to what is expected"""
    if pd.isnull(elem):
        return np.nan
    try:
        return str(elem)
    except:
        return np.nan

def toInt(elem):
    """Take an element as input and return the integer associated. Return np.nan if the element doesn't correspond to what is expected"""
    try:
        return int(elem)
    except:
        return np.nan

def toDate(elem, format):
    """Take an element and format he should parsed with as input and return the datetime associated. Return np.nan if the element doesn't correspond to what is expected"""
    try:
        return datetime.strptime(str(elem), format)
    except:
        return np.nan

def getFieldsFromSchema(path):
    """Return a field list using the path to the file containing a schema"""
    assert path.split('.')[-1] == "yaml", "Only .yaml file are accepted as a schema"

    with open(path, "r") as f:
        schema = yaml.safe_load(f)
    return schema[0]['fields']

def getColSetFromSchema(fields):
    """Take a field list as input and return a set of the fields names"""
    colSet = set()
    for field in fields:
        colSet.add(field['name'])
    return colSet

def applySchema(df, fields):
    for field in fields:
        if field['type'] == "string":
            df[field['name']] = df[field['name']].apply(toString).astype("string")
        elif field['type'] == "int":
            df[field['name']] = df[field['name']].apply(toInt).astype(float).astype('Int64')
        elif field['type'] == "date":
            assert 'format' in field.keys(), f"A format should be given when a date field is used. Not the case here {field}"
            df[field['name']] = df[field['name']].apply(lambda x : toDate(x, field['format'])).astype("datetime64[ns]")
        else:
            raise UnknownType(field['type'])
    return df

def load_csv(path, fields):
    """Load a csv with a path to the file and a fields list"""
    df = pd.read_csv(path)

    #test if the column set matches the schema
    if set(df.columns) != getColSetFromSchema(fields):
        raise SchemaNotMatchingData(f"Csv table schema {df.columns} is not matching the inputed schema {fields}")

    df = applySchema(df, fields)

    return df

def load_json(path, fields):
    """Load a csv with a path to the file and a fields list"""
    with open(path, 'r') as f:
        df = pd.DataFrame(json.load(f))

    #test if the column set matches the schema
    if set(df.columns) != getColSetFromSchema(fields):
        raise SchemaNotMatchingData(f"Json file schema {df.columns} is not matching the inputed schema {fields}")

    df = applySchema(df, fields)

    return df

def load(dataPath, schemaPath):
    """Load an input file with it's schema by taking the path to the file and the path to it's schema"""
    fields = getFieldsFromSchema(schemaPath)

    extension = dataPath.split('.')[-1]
    if extension == "csv":
        df = load_csv(dataPath, fields)
    elif extension == "json":
        df = load_json(dataPath, fields)
    else:
        raise NotHandledFileExtension(extension)
    return df