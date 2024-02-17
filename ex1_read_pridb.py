"""
Read pridb
==========
"""

#%%
import os

import matplotlib.pyplot as plt
import pandas as pd
import vallenae as vae

HERE = os.path.dirname(__file__) if "__file__" in locals() else os.getcwd()
PRIDB = os.path.join(HERE, "databases", "1p12_Ft_25000.pridb")

#%%
# Open pridb
# ----------
pridb = vae.io.PriDatabase(PRIDB)

print("Tables in database: ", pridb.tables())
print("Number of rows in data table (ae_data): ", pridb.rows())
print("Number of columns in data table (ae_data): ", pridb.columns())
print("Set of all channels: ", pridb.channel())

#%%
# Read hits to Pandas DataFrame
# -----------------------------
df_hits = pridb.iread_hits(query_filter="TRAI = 1")
#df_hits.to_csv("pridb_output.csv")
# Print a few columns
#print(df_hits.loc[df_hits['trai'] > 0])
for i in df_hits:
    print(i[11])

# %%
# Query Pandas DataFrame
# ----------------------
# DataFrames offer powerful features to query and aggregate data,
# e.g. plot summed energy per channel
ax = df_hits.groupby("channel").sum()["energy"].plot.bar(figsize=(8, 3))
ax.set_xlabel("Channel")
ax.set_ylabel("Summed Energy [eu = 1e-14 V²s]")
plt.tight_layout()

#%%
# Read markers
# ------------
df_markers = pridb.read_markers()
print(df_markers)

#%%
# Read parametric data
# --------------------
df_parametric = pridb.read_parametric()
print(df_parametric)
