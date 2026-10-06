import pandas as pd


def nan_replace_df(tabel):

    t = tabel.copy()

    for coloana in t.columns:
        if t[coloana].isna().sum() == 0:
            continue

        if pd.api.types.is_numeric_dtype(t[coloana]):
            t[coloana] = t[coloana].fillna(t[coloana].mean())
        else:
            t[coloana] = t[coloana].fillna(t[coloana].mode()[0])

    return t


def salvare_matrice(x, index_linie, index_coloana, fisier):

    t = pd.DataFrame(x, index=index_linie, columns=index_coloana)
    t.to_csv(fisier)


















