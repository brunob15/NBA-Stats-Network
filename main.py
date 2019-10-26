import players_graph as ply
import team_seasons_graph as ts
import bipartite as bip
import preprocessing as prep
import playoffs_prediction

[seasons_by_player, team_seasons, team_season_by_id] = prep.preprocess()

[bipartite_vtx, bipartite_edges] = bip.build_graph(team_seasons, seasons_by_player)
bip.export_csv(bipartite_vtx, bipartite_edges)

[players_vtx, players_edges] = ply.build_graph(team_seasons, seasons_by_player)
ply.export_csv(players_vtx, players_edges)

[ts_vtx, ts_edges] = ts.build_graph(team_seasons)
ts.export_csv(ts_vtx, ts_edges)
