import pandas as pd

def convert_csv_to_json():
    df = pd.read_csv('movies_initial.csv')
    df.to_json('movies.json', orient='records')

if __name__ == '__main__':
    convert_csv_to_json() 