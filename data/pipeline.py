import pandas as pd
import datetime

df = pd.read_csv( \
    'https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-ladesaulen-in-deutschland/exports/csv', \
    sep = ';'
    )

df.to_sql('ev_chargers_locations', 'sqlite:///data.sqlite', if_exists = 'replace', index=False)

# data only available until the end of last month
# download the latest info using last month (current month - 1)
last_month = datetime.datetime.now().month - 1
# data is on FZ 28.9 tab
xls = pd.read_excel( 
    f'https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_0{last_month}.xlsx?__blob=publicationFile&v=6',
    "FZ 28.9" 
    )

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


for i in range(len(metadata)):
    df.columns.values[i] = metadata[i]

df.to_sql('state_registered_vehicles', 'sqlite:///data.sqlite', if_exists = 'replace', index=False)