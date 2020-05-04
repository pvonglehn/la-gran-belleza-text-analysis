# Create a network graph of contributers to the magazine
# The nodes are the names of the contributers and the issues
# Edges are drawn between the contributers and issues, not between contributers
# Gephi was then used for the vizualization (see https://gephi.org/)


import pandas as pd
import networkx
import os
import pathlib

ROOT_DIR = pathlib.Path(__file__).parent.parent

structured_path = ROOT_DIR.joinpath("data","structured")
input_path = ROOT_DIR.joinpath(structured_path,"datos_para_link_relacional.xlsx")
output_path = ROOT_DIR.joinpath(structured_path,"graph.gexf")

# read data of contributers into dataframe
df = pd.read_excel(input_path)

# great a connected graph
graph = networkx.Graph()
# add edges between the magazine issues (TEMA) and names (NOMBRE)
_ = df.apply( lambda row: graph.add_edge(row["TEMA"],row["NOMBRE"]),axis=1)
# write to file for reading with Gephi
networkx.write_gexf(graph,output_path)