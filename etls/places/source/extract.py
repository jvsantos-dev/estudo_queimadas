import pandas as pd

def extract() -> pd.DataFrame:
    # coloquei o cainho onde estava o meu download, é impossível subir esse arquivo com o trabalho, então se quiser testar, vai ter que baixar o arquivo wildfires.csv do professor de datascience e colocar no caminho correto
    data = pd.read_csv(r"D:\Downloads\wildfires.csv", encoding='utf-8')
    return data
       