import lancedb
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

db = lancedb.connect("family_db")

data = [
    {"id": 1, "name": "Grandfather", "parent_id": None, "spouse": 2, "level": 0},
    {"id": 2, "name": "Grandmother", "parent_id": None, "spouse": 1, "level": 0},
    {"id": 3, "name": "Father", "parent_id": 1, "spouse": 4, "level": 1},
    {"id": 4, "name": "Mother", "parent_id": None, "spouse": 3, "level": 1},
    {"id": 5, "name": "Me", "parent_id": 3, "level": 2},
    {"id": 6, "name": "Brother", "parent_id": 3, "level": 2},
]

df = pd.DataFrame(data) 

table = db.create_table("family", df, mode="overwrite")    

family_df = table.to_pandas()                              
print(family_df)


G = nx.DiGraph()     

for _, row in family_df.iterrows():
    G.add_node(int(row["id"]))


for _, row in family_df.iterrows():    
    if pd.notna(row["spouse"]):
        G.add_edge(int(row["spouse"]), int(row["id"]))
    if pd.notna(row["parent_id"]):
        G.add_edge(int(row["parent_id"]), int(row["id"]))


pos = {}      

levels = family_df.groupby("level")      

for level, group in levels:
    x_positions = range(len(group))
    for i, row in enumerate(group.itertuples()):
        pos[int(row.id)] = (i, -level)


labels = dict(zip(family_df["id"], family_df["name"]))


fig, ax = plt.subplots(figsize=(10, 6))
nx.draw(
    G,
    pos,
    labels=labels,
    with_labels=True,
    node_size=5500,
    node_color="lightyellow",
    edgecolors="black",      
    linewidths=1.5,        
    font_size=11,
    arrows=True,
    arrowsize=10,
    ax=ax
)

ax.set_title("Family Tree using LanceDB", fontsize=14, pad=10)
ax.axis("off")
plt.margins(x=0.1, y=0.1)
plt.tight_layout()
plt.show()
