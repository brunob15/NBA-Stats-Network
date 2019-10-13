# NBA Stats Network 

## Overview
This project leverages **Network Analysis** concepts and techniques to predict the position reached by a team in a NBA season.

Also, some community detection algorithms are run to find the greatest combinations of players in NBA history.

## Techniques
**Statistical inference** techniques applied to network models are used to predict the position reached by a team in a season, based on the players that are part of the team and their stats in their stats in their NBA careers.
To achive this, a bipartite graph is created to model the player <-> team relationships and is labeled with some advanced player stats and the position reached by the team in regular season.

**Community detection** algorithms are run to find outstanding combinations of players like Jordan, Pippen and Rodman.
To achive this, a graph that models the players that were teammated is created and labeled with some advanced stats like Win Share, Box Plus Minus and Value Over Replacement.

## Dataset
This is the dataset used to get the NBA players stats: https://www.kaggle.com/drgilermo/nba-players-stats#Seasons_Stats.csv
The stats were scrapped from basketball-reference.com.
