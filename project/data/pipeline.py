import pandas as pd
import datetime
from googletrans import Translator

def get_current_month():
    return datetime.datetime.now().month

def extract_chargers_data(ev_chargers_src):
    df = pd.read_csv(ev_chargers_src, sep = ';')
    df[['latitude', 'longitude']] = df['koordinaten'].str.split(', ', expand=True)
    df = df.astype({"latitude": 'float64', "longitude": 'float64'})
    return df

def extract_ev_data():
    # data is on FZ 28.9 tab
    xls = None
    extracted = False
    latest_data_month = get_current_month() - 1 if get_current_month() - 1 > 0 else 12
    while not extracted and latest_data_month > 0:
        print("Trying to get data of month", latest_data_month)
        ev_src = f'https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_0{latest_data_month}.xlsx?__blob=publicationFile&v=6'
        try:
            xls = pd.read_excel( ev_src, "FZ 28.9" )
            extracted = True
        except Exception as e:
            print('--------------EXCEPTION---------------')
            print(e)
            print('--------------------------------------')
            latest_data_month -= 1
    if not extracted:
        raise Exception("No data available")
    # to-date data is on row 30 to 46 and col 1 onwards
    return xls.iloc[30:47, 1:]

def extract_kreis_data(kreis_src):
    df = pd.read_csv(kreis_src, sep = ';')
    df = df.loc[:, ["Land name", "Kreis name"]]
    return df

def add_metadata(df, metadata):
    for i in range(len(metadata)):
        df.columns.values[i] = metadata[i]
        
def load(df, table_name, db_name):
    df.to_sql(table_name, db_name, if_exists= 'replace', index = False)
    

if __name__ == '__main__':
    ev_chargers_src = 'https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-ladesaulen-in-deutschland/exports/csv'
    land_kries_src = 'https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-germany-kreis/exports/csv?lang=en&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B'
    
    df = extract_chargers_data(ev_chargers_src)
    lk_df = extract_kreis_data(land_kries_src)
    load(lk_df, 'land_landkreis', 'sqlite:///data.sqlite')
    load(df, 'ev_chargers_locations', 'sqlite:///data.sqlite')    

    # Extracting EV data
    df = extract_ev_data()
        
    metadata = [
            'state',
            'total_vehicle',
            'total_alternative',
            'alternative_drive_percentage',
            'total_electric_engine_vehicle',
            'electric_percentage',
            'electric_vehicle',
            'hydrogen_cell_vehicle',
            'plug_in_hybrid_vehicle',
            'total_hybrid_engine_vehicle',
            'full_hybrid_vehicle',
            'benzine_hybrid_vehicle',
            'benzine_full_hybrid_vehicle',
            'diesel_hybrid_vehicle',
            'diesel_full_hygrid_vehicle',
            'gas_vehicle',
            'hydrogen_vehicle'
            ]

    add_metadata(df,metadata)
    load(df, 'state_registered_vehicles', 'sqlite:///data.sqlite')

    