import pandas as pd
import os
import polars as pl
import logging

logger = logging.getLogger(__name__)

def load_to_dataframe(data) -> pd.DataFrame:
    """
    Loads data into DataFrame
    """
    if data is None or data.empty:
        logger.error("Empty Df !")
        raise ValueError("Empty DataFrame !")
    
    row_count = len(data)
    logger.info(f"Loaded DataFrame with {row_count} rows")

    return data

def load_to_polars(data) -> pl.DataFrame:
    """
    Loads data into Polars 
    """
    if data is None or data.empty:
        logger.error("Empty Df can't convert to Polars !")
        raise ValueError("Empty DataFrame !")
    
    row_count = len(data)
    logger.info(f"Converted DataFrame with {row_count} rows to Polars !")

    return pl.from_pandas(data)