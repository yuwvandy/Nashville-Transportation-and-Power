# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 09:55:01 2020

@author: 10624
"""

import networkx as nx
import osmnx as ox
import requests
import matplotlib.cm as cm
import matplotlib.colors as colors


place = {'city'   : 'Nashville',
         'state'  : 'Tennessee',
         'country': 'USA'}

G = ox.graph_from_place(place, network_type='drive', truncate_by_edge=True, custom_filter='["power"~"line"]')
fig, ax = ox.plot_graph(G, fig_height=10, node_size=0, bgcolor='k',
                        edge_color='orange', edge_linewidth=0.2)

nx.to_numpy_matrix(G)


G_proj = ox.project_graph(G)
nodes_proj = ox.graph_to_gdfs(G_proj, edges=False)
graph_area_m = nodes_proj.unary_union.convex_hull.area
ox.basic_stats(G_proj, area=graph_area_m, clean_intersects=True, circuity_dist='euclidean')

edge_centrality = nx.closeness_centrality(nx.line_graph(G))

G = ox.add_edge_speeds(G)
G = ox.add_edge_travel_times(G)
orig = ox.get_nearest_node(G, (36.158600, -86.978917))
dest = ox.get_nearest_node(G, (36.204046, -86.645208))
route = nx.shortest_path(G, orig, dest, weight='travel_time')
fig, ax = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k')