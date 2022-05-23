import pandas as pandas
import numpy as np
import itertools

YEAR_INDEX = 1
PLAYER_INDEX = 2
TEAM_INDEX = 5
MINUTES_PLAYED_INDEX = 8

dataset_path = 'Seasons_Stats.csv'
standings_path = 'team-season-positions.csv'

columnas = ['Year', 'Player', 'Tm', 'WS', 'PER']
dataset = pandas.read_csv(dataset_path, delimiter=',')[columnas]
dataset = dataset.rename(columns={'Tm': 'Team'})

# Cuando un jugador jugó en más de un equipo en la misma temporada
# hay una fila adicional con el valor TOT en la columna del equipo,
# que contiene el promedio de sus estadisticas en los equipos.
# Se eliminan estas filas.
dataset = dataset[(dataset.Team != 'TOT')]

# Eliminar filas vacías
dataset['Player'].replace('', np.nan, inplace=True)
dataset.dropna(subset=['Player'], inplace=True)

# Convertir año de float a integer
dataset['Year'] = pandas.to_numeric(dataset['Year'], downcast='integer')

def to_team_year(row):
    return row['Team'] + '-' + str(row['Year'])

dataset['TeamYear'] = dataset.apply(lambda row: to_team_year(row), axis=1)

# standings = pandas.read_csv(standings_path, delimiter=',')

dataset.to_csv("exported_csv/team_players.csv", index=False)
