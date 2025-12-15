import pytest
import pandas as pd
from ETL.transform import transform 

ALLOWED_DECISIONS = ["Recommended", "Partially recommended", "Anbefalet", "Delvist anbefalet"]

MOCK_DATA = pd.DataFrame({
    'decision': ["Recommended", "Rejected", "Anbefalet", "Pending", "Partially recommended"],
    'value': [1, 2, 3, 4, 5]
})

EXPECTED_DATA = pd.DataFrame({
    'decision': ["Recommended", "Anbefalet", "Partially recommended"],
    'value': [1, 3, 5]
}).reset_index(drop=True)

MOCK_EMPTY_DF = pd.DataFrame(columns=['decision', 'value'])

def test_transform_success_filtering():
    """Tests successful row filtering based on decision column"""
    
    result_df = transform(MOCK_DATA)
    
    assert isinstance(result_df, pd.DataFrame)
    
    assert len(result_df) == 3
    
    pd.testing.assert_frame_equal(result_df, EXPECTED_DATA)

def test_transform_no_allowed_decisions():
    """Tests transformation when no rows match the allowed decisions"""
    data_rejected = pd.DataFrame({'decision': ["Rejected", "Pending"], 'value': [10, 20]})
    
    result_df = transform(data_rejected)
    
    assert result_df.empty
    assert len(result_df) == 0

def test_transform_empty_input_returns_empty_df():
    """Tests that an empty input DF returns an empty DF"""
    
    result_df = transform(MOCK_EMPTY_DF)
    
    assert result_df.empty
    assert list(result_df.columns) == list(MOCK_EMPTY_DF.columns)

def test_transform_returns_dataframe():
    """Tests that the function always returns a DF object"""
    
    result_df = transform(MOCK_DATA)
    assert isinstance(result_df, pd.DataFrame)