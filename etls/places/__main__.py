from .source.extract import extract
from .source.transform import transform
from .source.load import load

def run(**kwargs):

    data = extract(**kwargs)
    transformed_data = transform(data, **kwargs)
    load(transformed_data, **kwargs)
    

if __name__ == '__main__':
    run()