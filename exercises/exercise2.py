import pandas as pd
import sqlalchemy
from abc import ABC, abstractmethod

class Block(ABC):
    @abstractmethod
    def execute(self,df):
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

class TrainstopsExtractor(Block):
    def __init__(self, source):
        self.source = source

    def execute(self):
        df = pd.read_csv(
                        self.source,
                        sep = ';',
                        decimal=','
                        )
        df.drop('Status', axis=1,inplace=True)
        df.dropna(inplace=True)
        return df

class TrainstopsTransformer(Block):
    def execute(self, df : pd.DataFrame):
        d = df
        #removing invalid verkehr
        valid_verkehr = ['FV','RV','nur DPN']
        print(d.shape)
        d = d[d["Verkehr"].isin(valid_verkehr)]
        print(d.shape)    
        
        #removing invalid laenge & breite
        d = d[((d['Laenge'] >= -90) & (d['Laenge'] <= 90))]
        d = d[((d['Breite'] >= -90) & (d['Breite'] <= 90))]
        print(d.shape)
        #removing invalid IFOPT
        pattern = r"^[a-zA-Z]{2}:\d+:\d+(:\d+)?$"
        d = d[d['IFOPT'].str.contains(pattern)]
        print(d.shape)
        #drop all rows with empty columns
        d = d.dropna(inplace=False)
        print(d.shape)
        return d
    
class TrainstopsDBLoader(Block):
    def __init__(self,table_name, db):
        self.table_name = table_name
        self.db = db
    
    def execute(self, df):
        sqlalchemy.create_engine(self.db)
        dtype={
            'EVA_NR' : sqlalchemy.INTEGER(),
            'DS100' : sqlalchemy.NVARCHAR(length=255),
            'IFOPT' : sqlalchemy.NVARCHAR(length=255),
            'NAME' : sqlalchemy.NVARCHAR(length=255),
            'Verkehr' : sqlalchemy.NVARCHAR(length=255),
            'Laenge' : sqlalchemy.FLOAT(),
            'Breite' : sqlalchemy.FLOAT(),
            'Betreiber_Name' : sqlalchemy.NVARCHAR(length=255),
            'Betreiber_Nr' : sqlalchemy.INTEGER(),
        }
        print(df)
        df.to_sql(self.table_name, self.db, dtype=dtype, if_exists= 'replace', index = False)
        return df


if __name__ == "__main__":
    source = "https://download-data.deutschebahn.com/static/datasets/haltestellen/D_Bahnhof_2020_alle.CSV"
    
    pipeline = DataPipeline(TrainstopsExtractor(source))
    pipeline.add_block(TrainstopsTransformer())
    pipeline.add_block(TrainstopsDBLoader('trainstops','sqlite:///trainstops.sqlite'))
    
    pipeline.execute()
    
