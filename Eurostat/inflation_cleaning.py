# MONATLICHE INFLATIONSDATEN von EUROSTAT


# Bibliotheken laden
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import eurostat


# monatliche inflationsdaten in einen dataframe laden
df_inf = eurostat.get_data_df("prc_hicp_manr")

# erste fünf Zeilen
df_inf.head()

# individuelle Variablen codes abrufen
df_inf["coicop"].unique()

# Inflaltion, Energie inflation und Food inflation
df_inf = df_inf[df_inf.coicop.isin(["CP00", "CP01", "CP02", "CP03", "CP04", "CP06", "CP07",
                                    "CP08", "CP09", "CP10", "CP11"])]


# Monate von Spalten in Zeilen
df_inf = df_inf.melt(id_vars=["freq", "unit", "coicop", "geo\TIME_PERIOD"],
               var_name="month",
               value_name="inflation"
               )


# Monat als Datum
df_inf["month"] = pd.to_datetime(df_inf["month"])

# relevante Spalten behalten
keep_cols = ["geo\TIME_PERIOD", "coicop", "month", "inflation"]
df_inf = df_inf[keep_cols]

# Spaltenlabels anpassen
colnames = ["country id", "category id", "month", "inflation"]
df_inf.columns = colnames

# erste fünf Zeilen
df_inf.head()

# Ländernamen hinzufügen

eu_countries = {
    "Belgium" : "BE",
    "Greece" : "EL",
    "Lithuania" : "LT",
    "Portugal" : "PT",
    "Bulgaria" : "BG",
    "Spain"	: "ES",
    "Luxembourg" : "LU",
    "Romania" : "RO",
    "Czechia" : "CZ",
    "France" : "FR",
    "Hungary" : "HU",
    "Slovenia" : "SI",
    "Denmark" : "DK",
    "Croatia" : "HR",
    "Malta"	: "MT",
    "Slovakia" : "SK",
    "Germany" : "DE",
    "Italy"	: "IT",
    "Netherlands" : "NL",
    "Finland" : "FI",
    "Estonia" : "EE",
    "Cyprus" : "CY",
    "Austria" : "AT",
    "Sweden" : "SE",
    "Ireland" : "IE",
    "Latvia" : "LV",
    "Poland" : "PL"
    }

non_eu_countries = {
    "Argentina" : "AR",
    "China :except Hong Kong" : "CN_X_HK",
    "Mexico" : "MX",
    "United Kingdom" : "UK",
    "United States" : "US",
    "Iceland" : "IS",
    "Norway" : "NO",
    "Liechtenstein" : "LI",
    "Switzerland" : "CH",
    "Bosnia and Herzegovina" : "BA",
    "Montenegro" : "ME",
    "Moldova" : "MD",
    "North Macedonia" : "MK",
    "Albania" : "AL",
    "Serbia" : "RS",
    "Turkey" : "TR",
    "Ukraine" : "UA",
    "Armenia" : "AM",
    "Belarus" : "BY",
    "Azerbaijan" : "AZ",
    "Kosovo" : "XK"
    }


# EU Länder - Namen hinzufügen

# tauschen von key und values im dictionary
d_swap = {v: k for k, v in eu_countries.items()}

# neue Spalte country hinzufügen
df_inf["country"] = np.nan
# Ländernamen mappen
df_inf.loc[:, "country"] = df_inf.loc[:, "country id"].map(d_swap)

# Spalte EU hinzufügen
df_inf["EU"] = True


# Nicht EU Länder - Namen hinzufügen

# tauschen von key und values im dictionary
d_swap = {v: k for k, v in non_eu_countries.items()}

# Länder ohne Eintrag identifizieren
mask = df_inf["country"].isnull()
# Ländernamen mappen
df_inf.loc[mask, "country"] = df_inf.loc[mask, "country id"].map(d_swap)

# Länder die nicht zur EU gehören klassifizieren
df_inf.loc[df_inf.country.isin(d_swap.values()), "EU"] = False


# Für Länder ohne Label die country id hinterlegen
df_inf.country.fillna(df_inf["country id"], inplace=True)



# inflation Kategorien labels hinzufügen
dic = {
    "CP00" : "overall",
    "CP01" : "food and drinks",
    "CP02" : "alcohol and tobacco",
    "CP03" : "clothes and shoes",
    "CP04" : "housing, water, electricity and other fuels",
    "CP06" : "health",
    "CP07" : "transport",
    "CP08" : "communication",
    "CP09" : "leisure and culture",
    "CP10" : "education",
    "CP11" : "restaurant and hotels",
    }

df_inf.loc[:, "category"] = df_inf.loc[:, "category id"].map(dic)


# Monat als Index
df_inf.set_index("month", inplace=True)

# Daten ab 2005
cutoff = "2005-01-01"
df_inf = df_inf[df_inf.index > cutoff]


# Spalten sortieren
cols = ["category id", "category", "country id", "country", "EU", "inflation"]
df_inf = df_inf[cols]


# Daten sortieren
df_inf = df_inf.sort_values(["category", "country", "EU"])

# plot data
df_inf[df_inf["country id"] == "NO"].groupby(["category"]).inflation.plot(legend=True)

# Datenformat
df_inf.shape

# Daten als excel Datei speichern
df_inf.to_excel("Daten/inflation.xlsx")


len(df_inf.loc[df_inf.EU == True, "country"].unique())
