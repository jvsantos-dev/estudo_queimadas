import pandas as pd

def extract() -> pd.DataFrame:
    data = pd.read_csv(r"D:\Downloads\wildfires.csv", encoding='utf-8')
    return data
       