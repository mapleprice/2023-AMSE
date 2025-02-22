# Project Plan

## Summary

This projects analyzes Electric Vehicles(EV) Charging stations and the numbers of newly registered vehicles, especially EV. and wether the stations are enough for EVs in the city. The study could reveal that the city/town does have enough stations for EV or not. The goal is provide an insight of future EV owners to decide if it is the right time for getting a new EV. Moreover, it is for the city/town to implement more charging stations to accommodate the increasing number of EV.

## Rationale

The analysis helps the relationship of EV charging stations and the registered vehicles to display which area or city that doesn't have enough charging stations. Therefore fixing the pain of not having enough EV charging stations and the for EV and could increase the number of charging stations so that more people will switch to EV Vehicles which could leads to less CO2 emissions.

## Datasources

<!-- Describe each datasources you plan to use in a section. Use the prefic "DatasourceX" where X is the id of the datasource. -->

### Datasource1: Neuzulassungen von Kraftfahrzeugen mit alternativem Antrieb (FZ 28) im Jahr 2023
* Metadata URL: https://mobilithek.info/offers/573357313572614144
* Data URL: https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_01.xlsx?__blob=publicationFile&v=3
* Data URL: https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_02.xlsx?__blob=publicationFile&v=6
* Data URL: https://www.kba.de/SharedDocs/Downloads/DE/Statistik/Fahrzeuge/FZ28/fz28_2023_03.xlsx?__blob=publicationFile&v=6
* Data Type: XLSX

As a result of notifications from the registration authorities in Germany, the Federal Motor Transport Authority (KBA) registers all newly registered vehicles in Germany in the Central Vehicle Register (ZFZR). In addition to vehicle-related data, such as brand, model series, fuel type, vehicle body, information about the owner and the registration process, such as the date of registration, is also transmitted. In addition to the monthly new registrations, the FZ 28 also lists the motor vehicles newly registered up to and including the reporting month for the entire year with regard to the alternative drive types electric (BEV), fuel cell (hydrogen), plug-in hybrid, hybrid, gas (liquid and natural gas) and hydrogen shown. Among other things, the characteristics of owner groups, brands, model series (top 10), segments and federal states are reported.


### Datasource2: Deutschland: E-Ladesäulen
* Metadata URL: https://mobilithek.info/offers/-2989425250318611078
* Data URL: https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-ladesaulen-in-deutschland/exports/shp
* Data URL: https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-ladesaulen-in-deutschland/exports/geojson
* Data URL: https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-ladesaulen-in-deutschland/exports/json
* Data URL: https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-ladesaulen-in-deutschland/exports/csv
* Data Type: SHP, GEOJSON, JSON, CSV

The data contains 36000+ instances of EV Charging stations which includes
- Provider name
- Latitude
- Longitude

### Datasource3: Kreise - Germany 
* Metadata URL: https://public.opendatasoft.com/explore/dataset/georef-germany-kreis/
* Data URL: https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/georef-germany-kreis/exports/csv?lang=en&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B
Data Type: CSV

This dataset is part of the Geographical repository maintained by Opendatasoft.

Processors and tools are using this data. They have been extracted from the Verwaltungsgebiete 1:250 000 (VG250) published by BKG, and contain data from 2020.

This dataset covers Germany at the Kreise (districts) level.

## Work Packages
<!-- List of work packages ordered sequentially, each pointing to an issue with more details. -->

1. Clean & Transform data [#1][i1]
2. Writing Automated Tests [#2][i2]
3. Deploy the Tests [#3][i3]
3. Exploratory Analysis [#4][i4]
4. Write Final Report [#5][i5]


[i1]: https://github.com/mapleprice/2023-AMSE/issues/1
[i2]: https://github.com/mapleprice/2023-AMSE/issues/2
[i3]: https://github.com/mapleprice/2023-AMSE/issues/3
[i4]: https://github.com/mapleprice/2023-AMSE/issues/4
[i5]: https://github.com/mapleprice/2023-AMSE/issues/5
