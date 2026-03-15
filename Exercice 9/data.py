import pandas as pd
import plotly.express as px

def get_stocks_data():
    df = px.data.stocks()
    df['date'] = pd.to_datetime(df['date'])
    return df

def get_gapminder_data():
    url = "https://gist.githubusercontent.com/fluret/ac9448085ca978b65f8f53535d2caa97/raw/216956a76aa5625b57f95af3bab97ea0d9ec8b24/data_03.txt"
    df = pd.read_csv(url, sep=';', decimal=',')
    return df

# Mapping des métriques pour Gapminder
METRICS_MAP = {
    'Population': {'col': 'pop', 'agg': 'sum'},
    'PIB par habitant': {'col': 'gdpPercap', 'agg': 'mean'},
    'Espérance de vie': {'col': 'lifeExp', 'agg': 'mean'}
}