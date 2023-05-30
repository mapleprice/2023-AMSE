import pandas as pd
import datetime

def get_current_month():
    return datetime.datetime.now().month

def add_metadata(df, metadata):
    for i in range(len(metadata)):
        df.columns.values[i] = metadata[i]
    

ev_chargers_src = 'https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-ladesaulen-in-deutschland/exports/csv'
registered_cars_src = f'https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_0{get_current_month() - 1}.xlsx?__blob=publicationFile&v=6'

if __name__ == '__main__':
    
    df = pd.read_csv( ev_chargers_src, sep = ';')
    df.to_sql('ev_chargers_locations', 'sqlite:///data.sqlite', if_exists = 'replace', index=False)

    # data is on FZ 28.9 tab
    xls = pd.read_excel( registered_cars_src, "FZ 28.9" )
    # to-date data is on row 30 to 46 and col 1 onwards
    df = xls.iloc[30:47, 1:]
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
    # add metadata
    add_metadata(df,metadata)
    #save to database
    df.to_sql('state_registered_vehicles', 'sqlite:///data.sqlite', if_exists = 'replace', index=False)

    