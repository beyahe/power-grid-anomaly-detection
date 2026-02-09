import pandas as pd

df = pd.read_csv("data/clean/clean_power_data.csv")

NUM_VILLAGES = 5

df["village_id"] = df.index % NUM_VILLAGES

for i in range(NUM_VILLAGES):
    village_df = df[df["village_id"] == i]
    village_df.to_csv(f"data/villages/village_{i}.csv", index=False)

print("تم تقسيم البيانات إلى قرى")
