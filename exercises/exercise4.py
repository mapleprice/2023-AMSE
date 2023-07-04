import pandas as pd
import sqlalchemy
from abc import ABC, abstractmethod
import urllib.request as request
import zipfile


class Block(ABC):
    @abstractmethod
    def execute(self, df):
        pass


class DataPipeline:
    def __init__(self, extractor):
        self.pipeline = []
        self.extractor = extractor

    def add_block(self, block: Block):
        self.pipeline.append(block)

    def execute(self):
        df = self.extractor.execute()
        for block in self.pipeline:
            df = block.execute(df)
        return df
    
#==============================================================================

class TemperatureZipRetreiver(Block):
    def __init__(self, source):
        self.source = source

    def execute(self):
        zipf = request.urlretrieve(self.source)
        
        zipf = zipf[0]
        
        zipf = zipfile.ZipFile(zipf, 'r')
        zipf.extractall(".")
        return zipf


class TemperaturesExtractor(Block):
    def execute(self, df):
        df = pd.read_csv("data.csv", sep=';', decimal=',', header = None, usecols=range(0,11))
        df.columns = df.iloc[0]
        df.drop(index= 0, inplace=True)
        return df

class TemperaturesReshaper(Block):
    def execute(self, df):
        d = df
        # selecting useful columns
        valid_columns = ["Geraet", "Hersteller", "Model", "Monat",
                         "Temperatur in °C (DWD)", "Batterietemperatur in °C", "Geraet aktiv"]
        d = d[valid_columns]
        d.rename(columns={"Temperatur in °C (DWD)": "Temperatur", "Batterietemperatur in °C" : "Batterietemperatur"}, inplace=True)
        return d
    
    
class TemperaturesTransformer(Block):
    def execute(self, df: pd.DataFrame):
        d = df
        
        d["Temperatur"] = d["Temperatur"].apply(lambda x: x.replace(',', '.')).astype(float)
        d["Temperatur"] = d["Temperatur"].apply(lambda x: round((x * 9/5) + 32,2))
        
        d["Batterietemperatur"] = d["Batterietemperatur"].apply(lambda x: x.replace(',', '.')).astype(float)
        d["Batterietemperatur"] = d["Batterietemperatur"].apply(lambda x: round((x * 9/5) + 32,2))
        
        d["Geraet"] = d["Geraet"].astype(int)
        d = d[d["Geraet"] > 0]

        d = d.dropna(inplace=False)
        return d
        


class TemperaturesDBLoader(Block):
    def __init__(self, table_name, db):
        self.table_name = table_name
        self.db = db

    def execute(self, df):
        dtype = {
            'Geraet': sqlalchemy.types.Integer(),
            'Hersteller': sqlalchemy.types.String(length=255),
            'Model': sqlalchemy.types.String(length=255),
            'Monat': sqlalchemy.types.Integer(),
            'Temperatur': sqlalchemy.types.Float(),
            'Batterietemperatur': sqlalchemy.types.Float(),
            'Geraet aktiv': sqlalchemy.types.String(length=255),
        }
        print(df)
        df.to_sql(self.table_name, self.db, dtype=dtype,
                  if_exists='replace', index=False)
        return df


if __name__ == "__main__":
    source = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
    
    pipeline = DataPipeline(TemperatureZipRetreiver(source))
    pipeline.add_block(TemperaturesExtractor())
    pipeline.add_block(TemperaturesReshaper())
    pipeline.add_block(TemperaturesTransformer())
    pipeline.add_block(TemperaturesDBLoader(
        'Temperatures', 'sqlite:///temperatures.sqlite'))

    pipeline.execute()
