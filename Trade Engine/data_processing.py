import pandas as pd

def preprocess_data(data):
    data = data.fillna(method='ffill')
    data = data.dropna()
    return data
