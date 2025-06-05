def transform(data):
    import pandas as pd
    import numpy as np
    data = data.drop_duplicates()
    data = data.dropna()

    rename_columns = {
        'STATE': 'estado',
        'NWCG_GENERAL_CAUSE': 'causa',
        'DISCOVERY_DATE': 'data',
        'LATITUDE': 'latitude',
        'LONGITUDE': 'longitude'
    }
    # Normalizando as categorias e campos de datas

    data['CONT_DATE'] = pd.to_datetime(data['CONT_DATE'], errors='coerce')
    data['DISCOVERY_DATE'] = pd.to_datetime(data['DISCOVERY_DATE'], errors='coerce')
    data['FIRE_NAME'] = data['FIRE_NAME'].astype(str)

    # Normalizando os outliers, passando eles como um filtro para tirar os que estiverem dentro desse filtro estabelecido

    colunas_numericas = data.select_dtypes(include=['int64', 'float64']).columns

    Q1 = data[colunas_numericas].quantile(0.25)
    Q3 = data[colunas_numericas].quantile(0.75)

    IQR = Q3 - Q1

    filtro = ~((data[colunas_numericas] < (Q1 - 1.5 * IQR)) |
            (data[colunas_numericas] > (Q3 + 1.5 * IQR))).any(axis=1)
    
    normalized_data = data[filtro].copy()
    columns = ['STATE', 'NWCG_GENERAL_CAUSE', 'DISCOVERY_DATE', 'LATITUDE', 'LONGITUDE']
    transformed_data = normalized_data[columns].copy()
    transformed_data.rename(columns=rename_columns, inplace=True)
    transformed_data = transformed_data.drop_duplicates(subset=['latitude', 'longitude'])
    transformed_data['data'] = transformed_data['data'].dt.strftime('%Y-%m-%d')

    #Usando o sample para pegar apenas 10.000 linhas, pois fica muito pesado para processar o arquivo inteiro
    transformed_data = transformed_data.sample(n=10000, replace=False).copy()
    return transformed_data