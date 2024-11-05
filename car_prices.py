import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


st.title('Car Prices Clean')
# Chargement des données
@st.cache_data
def load_data():
    data = pd.read_csv("/home/isalog/Brief8/car_prices_clean.csv")
    #data['make'] = data['make'].astype('category')
    return data

#st.write(car_prices.dtypes)
data_load_state = st.text('Chargement des données...')
car_prices = load_data()
data_load_state.text('Chargement des données... terminé!')

# Affichez le tableau complet
st.subheader('Données brutes')
st.dataframe(car_prices)

#Selection de la colonne pour le tri
option = st.selectbox(
    "Sur quelle colonne voulez_vous effectuer le tri?",
    ("year", "make", "model","trim", "body", "transmission","state","condition","color", "interior", "seller","mmr","sellingprice","saledate" ),
)
# bouton radio pour selectionner l'ordre de tri
sort_order = st.radio( "Selectionnez l'ordre de tri:",
                      ("Ascendant","Descendant"))

st.write(f"Vous avez selectionné: {option} en ordre {sort_order.lower()}" )

# Tri des données
ascending = sort_order == "Ascendant"
sorted_data = car_prices.sort_values(by=option, ascending=ascending)

# Affichage des données triées
st.subheader(f'Données triées par {option} en ordre {sort_order.lower()}')
st.dataframe(sorted_data)

# Filtrage par marque
st.subheader('Filtrer par marque')
all_makes = car_prices['make'].unique()
selected_makes = st.multiselect("Choisissez une ou plusieurs marques", options=all_makes)

if selected_makes:
    filtered_data = car_prices[car_prices['make'].isin(selected_makes)]
    st.subheader('Données filtrées par marque')
    st.dataframe(filtered_data)
else:
    st.write("Aucune marque sélectionnée. Veuillez choisir au moins une marque pour filtrer les données.")

#Creation de filtres pour les données numériques
# Filtrage pour les données numériques ('year')
st.subheader('Filtrer par année')

# Obtenir les valeurs min et max de la colonne 'year'
min_year = int(car_prices['year'].min())
max_year = int(car_prices['year'].max())

# Créer un slider pour sélectionner la plage d'années'
year_range = st.slider(
    "Sélectionnez la plage d' années",
    min_value=min_year,
    max_value=max_year,
    value=(min_year, max_year)  # valeur par défaut
)
# Filtrer les données en utilisant pandas.Series.between()
filtered_by_year = car_prices[car_prices['year'].between(year_range[0], year_range[1])]

# Afficher les résultats
st.subheader('Voitures filtrées par année')
st.dataframe(filtered_by_year)

# Afficher le nombre de voitures dans la plage des années sélectionnées
st.write(f"Nombre de voitures dans la plage d'années : {len(filtered_by_year)}")

# Filtrage pour les données numériques ('odometer')
st.subheader('Filtrer par kilometrage')

# Obtenir les valeurs min et max de la colonne 'odometer'
min_odometer = int(car_prices['odometer'].min())
max_odometer = int(car_prices['odometer'].max())

# Créer un slider pour sélectionner la plage de kilomètres'
odometer_range = st.slider(
    "Sélectionnez la durée en années",
    min_value=min_odometer,
    max_value=max_odometer,
    value=(min_year, max_year)  # valeur par défaut
)
# Filtrer les données en utilisant pandas.Series.between()
filtered_by_odometer = car_prices[car_prices['odometer'].between(odometer_range[0], odometer_range[1])]

# Afficher les résultats
st.subheader('Voitures filtrées par km')
st.dataframe(filtered_by_odometer)

# Afficher le nombre de voitures dans la plage des km sélectionnés
st.write(f"Nombre de voitures dans la plage de km : {len(filtered_by_odometer)}")

# Filtrage pour les données numériques ('mmr')
st.subheader('Filtrer par le prix marché')

# Obtenir les valeurs min et max de la colonne 'odometer'
min_mmr = int(car_prices['mmr'].min())
max_mmr = int(car_prices['mmr'].max())

# Créer un slider pour sélectionner la plage de kilomètres'
mmr_range = st.slider(
    "Sélectionnez la durée en années",
    min_value=min_mmr,
    max_value=max_mmr,
    value=(min_mmr, max_mmr)  # valeur par défaut
)
# Filtrer les données en utilisant pandas.Series.between()
filtered_by_mmr = car_prices[car_prices['mmr'].between(mmr_range[0], mmr_range[1])]

# Afficher les résultats
st.subheader('Voitures filtrées par prix du marché')
st.dataframe(filtered_by_mmr)

# Afficher le nombre de voitures dans la plage des prix du marché sélectionés 
st.write(f"Nombre de voitures dans la plage des prix du marché : {len(filtered_by_mmr)}")

# Filtrage pour les données numériques ('sellingprice')
st.subheader('Filtrer par prix de vente')

# Obtenir les valeurs min et max de la colonne 'sellingprice'
min_price = int(car_prices['sellingprice'].min())
max_price = int(car_prices['sellingprice'].max())

# Créer un slider pour sélectionner la plage de prix
price_range = st.slider(
    "Sélectionnez la plage de prix",
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price)  # valeur par défaut
)
# Filtrer les données en utilisant pandas.Series.between()
filtered_by_price = car_prices[car_prices['sellingprice'].between(price_range[0], price_range[1])]

# Afficher les résultats
st.subheader('Voitures filtrées par prix de vente')
st.dataframe(filtered_by_price)

# Afficher le nombre de voitures dans la plage de prix sélectionnée
st.write(f"Nombre de voitures dans la plage de prix sélectionnée : {len(filtered_by_price)}")

# Filtrage pour les données numériques ('saledate')
# Mise au format datetime de la colonne 'saledate' 
car_prices['saledate'] = pd.to_datetime(car_prices['saledate'])

st.subheader('Filtrer par date de vente')

#Créer un slider pour selectioner la plage de date
start_date, end_date = st.slider("Sélectionnez la plage de dates", 
                                 min_value=car_prices['saledate'].min().date(),
                                 max_value=car_prices['saledate'].max().date(),
                                 value=(car_prices['saledate'].min().date(), car_prices['saledate'].max().date()))
start_date = pd.Timestamp(start_date).tz_localize('UTC')
end_date = pd.Timestamp(end_date).tz_localize('UTC')

filtered_by_date = car_prices[(car_prices['saledate'] >= start_date) & (car_prices['saledate'] <= end_date)]


# Afficher les résultats
st.subheader('Voitures filtrées par date de vente')
st.dataframe(filtered_by_date)

# Afficher le nombre de voitures dans la plage de prix sélectionnée
st.write(f"Nombre de voitures dans la plage de date sélectionnée : {len(filtered_by_date)}")

















