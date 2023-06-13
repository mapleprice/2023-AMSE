import pandas as pd
import datetime

def get_current_month():
    return datetime.datetime.now().month

def extract_chargers_data(ev_chargers_src):
    df = pd.read_csv(ev_chargers_src, sep = ';')
    df[['latitude', 'longitude']] = df['koordinaten'].str.split(', ', expand=True)
    df = df.astype({"latitude": 'float64', "longitude": 'float64'})
    return df

def extract_ev_data(ev_src):
    # data is on FZ 28.9 tab
    xls = pd.read_excel( ev_src, "FZ 28.9" )
    # to-date data is on row 30 to 46 and col 1 onwards
    return xls.iloc[30:47, 1:]

def add_metadata(df, metadata):
    for i in range(len(metadata)):
        df.columns.values[i] = metadata[i]
        
def load(df, table_name, db_name):
    df.to_sql(table_name, db_name, if_exists= 'replace', index = False)
    

ev_chargers_src = 'https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-ladesaulen-in-deutschland/exports/csv'
registered_cars_src = f'https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_0{get_current_month() - 1}.xlsx?__blob=publicationFile&v=6'

if __name__ == '__main__':
    
    df = extract_chargers_data(ev_chargers_src)
    load(df, 'ev_chargers_locations', 'sqlite:///data.sqlite')

    # Extracting EV data
    extracted = False
    latest_data_month = get_current_month() - 1
    while not extracted:
        print("Trying to get data of month", latest_data_month)
        registered_cars_src = f'https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_0{latest_data_month}.xlsx?__blob=publicationFile&v=6'
        try:
            df = extract_ev_data(registered_cars_src)
            extracted = True
        except Exception:
            latest_data_month -= 1
        
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

    