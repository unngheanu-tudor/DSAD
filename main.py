import os
import pandas as pd
from scipy.spatial.distance import cdist

from functii_online import nan_replace_df, salvare_matrice

# folder maker
os.makedirs("data_out", exist_ok=True)

# 1
# Varianta UCI foloseste ";" ca separator, varianta Kaggle foloseste ",".
# Incercam intai cu ";" si, daca iese o singura coloana, reincercam cu ",".
tabel = pd.read_csv("winequality-red.csv", sep=";")
if tabel.shape[1] == 1:
    tabel = pd.read_csv("winequality-red.csv", sep=",")

print("Cerinta 1")
print("shape:", tabel.shape)
print(tabel.head())
print(tabel.dtypes)

# 2
tabel = nan_replace_df(tabel)
print("\nCerinta 2")
print("Numar de NaN ramase:", tabel.isna().sum().sum())  # trebuie sa fie 0

# 3 filt
bune = tabel[tabel["quality"] >= 7]
bune.to_csv("data_out/vinuri_calitate_min7.csv", index=False)

# 4
top50 = tabel.sort_values("alcohol", ascending=False).head(50)
top50.to_csv("data_out/top50_alcool.csv", index=False)

# 5
medii = tabel.groupby("quality")[["alcohol", "pH"]].mean()
medii = medii.reset_index()  # "quality" devine coloana normala, un rand per nota
medii.to_csv("data_out/medii_pe_calitate.csv", index=False)

# 6
tabel["aciditate_totala"] = (
    tabel["fixed acidity"] + tabel["volatile acidity"] + tabel["citric acid"]
)
rezultat6 = tabel[["quality", "alcohol", "aciditate_totala", "pH"]]
rezultat6.to_csv("data_out/vinuri_cu_aciditate.csv", index=False)


#7
rand_max = medii["alcohol"].idxmax()
nota_max = medii.loc[rand_max, "quality"]
pd.DataFrame({"quality": [nota_max]}).to_csv(
    "data_out/calitate_max_alcool.csv", index=False
)
print("\nCerinta 7")
print("Nota cu media alcoolului maxima:", nota_max)

#8
coloane_corr = [
    "fixed acidity",
    "volatile acidity",
    "citric acid",
    "alcohol",
    "quality",
]
R = tabel[coloane_corr].corr()
salvare_matrice(R.values, R.index, R.columns, "data_out/R.csv")

# ---------------------------------------------------------------

media_alcool = tabel["alcohol"].mean()
std_alcool = tabel["alcohol"].std(ddof=0)
tabel["alcohol_std"] = (tabel["alcohol"] - media_alcool) / std_alcool
tabel[["alcohol", "alcohol_std"]].to_csv(
    "data_out/alcohol_standardizat.csv", index=False
)




#10
coloane_dist = ["fixed acidity", "volatile acidity", "alcohol"]
primele20 = tabel[coloane_dist].head(20)

primele20_std = (primele20 - primele20.mean()) / primele20.std(ddof=0)

d = cdist(primele20_std.values, primele20_std.values, metric="euclidean")
salvare_matrice(d, primele20_std.index, primele20_std.index, "data_out/d_euclid_20.csv")

print("\nFisierele sunt in folderul data_out.")