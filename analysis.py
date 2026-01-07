import numpy as np
import pandas as pd

np.random.seed(42)

data = np.random.normal(loc=0, scale=1, size=1000)
df = pd.DataFrame({"value": data})

print("Mean:", df["value"].mean())
print("Std:", df["value"].std())

# Added a new line to print the number of rows
print("Rows:", len(df))
