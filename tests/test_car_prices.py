""" test_car_prices.py"""
from streamlit.testing.v1 import AppTest
from datetime import date

at = AppTest.from_file("car_prices.py",default_timeout=10).run()

def test_titre():
    assert "Ventes de voitures aux Etats Unis" in at.title[0].value 

def test_filtre_premier():
    assert "Trier les lignes" in at.sidebar.subheader[0].value

def test_colonne():
    assert at.selectbox[0].value == "ANNEE"

def test_ordre_tri():
    assert at.radio [0].value == "Ascendant"

#Vérification si des colonnes sont disponibles pour le filtrage
def test_ajout_filtre():
    at.sidebar.selectbox[0].value == "ANNEE"
    assert at.sidebar.selectbox[1].value == "MARQUE"

#Date de vente
def test_date_de_vente():
    date_range = at.date_input[0].value
    assert isinstance(date_range, tuple)
    assert len(date_range) == 2
    assert date_range[0] == date(2014, 1, 1)
    assert date_range[1] == date(2015, 7, 21)



