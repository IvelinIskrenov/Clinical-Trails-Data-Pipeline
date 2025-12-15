import pytest
import pandas as pd
import polars as pl
from ETL.load import load_to_dataframe, load_to_polars 

MOCK_DATA = pd.DataFrame({'id': [1], 'value': ['A']})
MOCK_EMPTY_DF = pd.DataFrame()

#Pandas

def test_dataframe_success():
    """Tests successful Pandas DataFrame loading"""
    result = load_to_dataframe(MOCK_DATA)
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1

def test_dataframe_empty_input_raises_valueerror():
    """Tests ValueError on empty input DF"""
    with pytest.raises(ValueError):
        load_to_dataframe(MOCK_EMPTY_DF)

def test_dataframe_none_input_raises_valueerror():
    """Tests ValueError on None input"""
    with pytest.raises(ValueError):
        load_to_dataframe(None)

# Polars

def test_polars_success():
    """Tests successful conversion to Polars DF"""
    result = load_to_polars(MOCK_DATA)
    assert isinstance(result, pl.DataFrame)
    assert result.height == 1

def test_polars_empty_input_raises_valueerror():
    """ПTests ValueError on empty Pandas DF conversion"""
    with pytest.raises(ValueError):
        load_to_polars(MOCK_EMPTY_DF)

def test_polars_none_input_raises_valueerror():
    """Tests ValueError on None input for Polars conversion"""
    with pytest.raises(ValueError):
        load_to_polars(None)