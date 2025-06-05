def load(transformed_data):
    import pandas as pd
    import json
    # Convert the list of dictionaries to a DataFrame
    grouped = {}
    for state, group in transformed_data.groupby('estado'):
        grouped[state] = group[['latitude', 'longitude', 'data']].to_dict(orient='records')

    # Agora salvando o dicionário 'grouped', não o DataFrame
    with open(r'D:\Desktop\EstudoQueimadas\json\places.json', 'w', encoding='utf-8') as file:
        json.dump(grouped, file, indent=2, ensure_ascii=False)