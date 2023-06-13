from numpy import NaN
import pandas as pd
from data.pipeline import *
from unittest import TestCase
import sqlite3

from pandas.testing import assert_frame_equal

class UnitTest(TestCase):
    def test_add_metadata(self):
        data = pd.DataFrame([[1,2,3],[2,3,4],[5,6,7]], columns=['null','null','null'])
        
        test_data = pd.DataFrame([[1,2,3],[2,3,4],[5,6,7]], columns=['ab','ba','cc'])
        add_metadata(data, ['ab','ba','cc'])
        assert_frame_equal(test_data, data)

        
    def test_load(self):
        data = pd.DataFrame([[4,5,6],[1,2,3]], columns=['a','b','c'])
        load(data,'test_load' ,'sqlite:///test_load.sqlite')
        
        conn = sqlite3.connect('test_load.sqlite')
        result = pd.read_sql_query("SELECT * FROM test_load", conn)
        conn.close()
        
        assert_frame_equal(result, data)
    