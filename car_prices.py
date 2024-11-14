import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import io


# Titre de l'application
st.title('Ventes de voitures aux Etats Unis')

# Définition de la fonction pour charger les données avec le décorateur st.cache_data
@st.cache_data
def load_data():
    # Charger les données du fichier CSV
    data = pd.read_csv("/home/isalog/Brief8/car_prices_clean.csv")
    # Conversion de la colonne 'saledate' en type datetime
    data['saledate'] = pd.to_datetime(data['saledate'],utc = True)
    return data

# Fonction pour convertir les dates au format naif et utile pour exporter le fichier excel
def convert_to_naive_datetime(df):
    for col in df.select_dtypes(include=['datetime64[ns, UTC]']).columns:
        df[col] = df[col].dt.tz_localize(None)
    return df

# Chargement des données
df = load_data()

df.rename(index=str,columns={"year":"ANNEE",
                              "make":"MARQUE",
                              "model":"MODELE",
                              "trim":"FINITION",
                              "body":"TYPE",
                              "transmission":"TRANSMISSION",
                              "state":"ETAT",
                              "condition":"EVALUATION_ETAT",
                              "odometer":"COMPTEUR",
                              "color":"COULEUR",
                              "interior":"COULEUR_INT",
                              "seller":"VENDEUR",
                              "mmr": "VALEUR_MARCHE",
                              "sellingprice":"PRIX_VENTE",
                              "saledate":"DATE_VENTE"

}, inplace=True)

# Premier filtre : Tri des données
st.sidebar.subheader("Trier les lignes")
sort_column = st.sidebar.selectbox("Trier sur cette colonne", df.columns)
sort_order = st.sidebar.radio("Ordre de tri", ["Ascendant", "Descendant"])
ascending = sort_order == "Ascendant"

# Appliquer le tri
sorted_car_prices = df.sort_values(by=sort_column, ascending=ascending)
name_columns = ["ANNEE","MARQUE","MODELE", "FINITION","TYPE","TRANSMISSION","ETAT","EVALUATION_ETAT","COMPTEUR","COULEUR","COULEUR_INT","VENDEUR","VALEUR_MARCHE","PRIX_VENTE","DATE_VENTE"]
# Deuxième filtre : Filtrer les données selon le choix du premier filtre
st.sidebar.subheader("Filtrer les lignes")

 #Création de la liste des colonnes disponibles pour le filtrage
available_columns = [col for col in df.columns if col != sort_column]

# Vérification si des colonnes sont disponibles pour le filtrage
if available_columns:
    filter_column = st.sidebar.selectbox("Ajouter un filtre", options=available_columns)
    #st.write("Colonne de filtre sélectionnée:", filter_column)
else:
    #st.warning("Aucune colonne disponible pour le filtrage.")
    filter_column = None


#vérification de sort_column
#st.write("sort_column:", sort_column)

# Appliquer le deuxième filtre en fonction du type de données
#verification de la valeur de 'filter_column'
#st.write("filter_column:", filter_column)
if pd.api.types.is_numeric_dtype(sorted_car_prices[filter_column]):
    min_val, max_val = float(sorted_car_prices[filter_column].min()), float(sorted_car_prices[filter_column].max())
    filter_range = st.sidebar.slider(f"Filtrer par {filter_column}", min_val, max_val, (min_val, max_val))
    filtered_car_prices = sorted_car_prices[sorted_car_prices[filter_column].between(*filter_range)]
elif pd.api.types.is_datetime64_any_dtype(sorted_car_prices[filter_column]):
    min_date, max_date = sorted_car_prices[filter_column].min().date(), sorted_car_prices[filter_column].max().date()
    start_date, end_date = st.sidebar.date_input(f"Filtrer par {filter_column}", (min_date, max_date))
    filtered_car_prices = sorted_car_prices[(sorted_car_prices[filter_column].dt.date >= start_date) & 
                                             (sorted_car_prices[filter_column].dt.date <= end_date)]
else:
    unique_values = sorted_car_prices[filter_column].unique()
    selected_values = st.sidebar.multiselect(f"Filtrer par {filter_column}", options=unique_values)
    if selected_values:
        filtered_car_prices = sorted_car_prices[sorted_car_prices[filter_column].isin(selected_values)]
    else:
        filtered_car_prices = sorted_car_prices


# Filtrage par date de vente
date_range = st.sidebar.date_input("Dates de vente", 
                                    [df['DATE_VENTE'].min().date(), df['DATE_VENTE'].max().date()],
                                    min_value=df['DATE_VENTE'].min().date(),
                                    max_value=df['DATE_VENTE'].max().date(),
                                    key="date_filter")

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_car_prices = filtered_car_prices[(filtered_car_prices['DATE_VENTE'].dt.date >= start_date) & 
                                               (filtered_car_prices['DATE_VENTE'].dt.date <= end_date)]

# Filtrage par prix de vente
price_range = st.sidebar.slider("Prix de vente", 
                                int(df['PRIX_VENTE'].min()), int(df['PRIX_VENTE'].max()), 
                                (int(df['PRIX_VENTE'].min()), int(df['PRIX_VENTE'].max())))
filtered_car_prices = filtered_car_prices[filtered_car_prices['PRIX_VENTE'].between(*price_range)]

#Group BY
st.subheader("Analyse GroupBy")

# Sélection de la colonne pour le groupby
groupby_column = st.selectbox("Choisissez la colonne pour le groupby", df.columns)


# Sélection des colonnes pour l'agrégation
columns_for_agg = ["COMPTEUR", "VALEUR_MARCHE", "PRIX_VENTE"]
selected_columns = st.multiselect("Sélectionnez les colonnes pour l'agrégation", columns_for_agg)
if selected_columns:
# Sélection de la fonction d'agrégation
    agg_function = st.selectbox("Choisissez la fonction d'agrégation", ["Somme","Moyenne", "Maximum", "Minimum"])
    
# Effectuer le groupby
    if agg_function == "Somme":
        grouped_data = filtered_car_prices.groupby(groupby_column)[selected_columns].sum()
    elif agg_function == "Moyenne":
        grouped_data = filtered_car_prices.groupby(groupby_column)[selected_columns].mean()
    elif agg_function == "Maximum":
        grouped_data = filtered_car_prices.groupby(groupby_column)[selected_columns].max()
    else:
         grouped_data = filtered_car_prices.groupby(groupby_column)[selected_columns].min()
    
# Afficher les résultats
    st.write(f"{agg_function} par {groupby_column}:")
    st.dataframe(grouped_data)



# Affichage du tableau filtré avec streamlit.dataframe()
st.subheader('Données filtrées')
st.dataframe(filtered_car_prices)

# Conversion des dates en format naive pour pouvoir télécharger le fichier sous Excel
filtered_car_prices = convert_to_naive_datetime(filtered_car_prices)

#création d'un buffer en mémoire pour télécharger
#buffer = io.BytesIO()
#Ecriture du DataFrame dans le buffer au format Excel
#with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
#    filtered_car_prices.to_excel(writer, sheet_name='Sheet1', index=False)

#Création du bouton de téléchargement
#st.download_button(
#    label="Télécharger le fichier Excel",
 #   data=buffer.getvalue(),
 #   file_name="donnees_filtrees.xlsx",
# mime="application/vnd.ms-excel"










