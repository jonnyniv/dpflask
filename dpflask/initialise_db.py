from dpflask import db
import pandas as pd


def create_db():
    connection = db.connect_db()
    dataset = pd.read_json('https://data.iowa.gov/resource/wxib-fsgn.json?$limit=50000&$order=:id')
    dataset = dataset.drop('primary_county_coordinates', 1)
    dataset['month'] = dataset['date'].dt.month
    print(dataset.head())
    dataset.to_sql('dpflask', connection, if_exists='replace')
    connection.commit()
    connection.close()


if __name__ == '__main__':
    create_db()
