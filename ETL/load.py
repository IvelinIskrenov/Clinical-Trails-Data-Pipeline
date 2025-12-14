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

def load_to_csv(data: pd.DataFrame, output_path: str):
    """
    Loads data into a CSV file
    """
    if data is None or data.empty:
        logger.error("Empty Df can't convert to CSV !")
        raise ValueError("Empty DataFrame !")

    os.makedirs(os.path.dirname(output_path), exist_ok = True)

    data.to_csv(
        output_path,
        index=False,
        encoding="utf-8"
    )
    logger.info(f"Saved DataFrame with {len(data)} rows to CSV at '{output_path}' !")

def load_to_polars(df) -> pl.DataFrame:
    """
    Loads data into Polars 
    """
    if df is None or df.empty:
        logger.error("Empty Df can't convert to Polars !")
        raise ValueError("Empty DataFrame !")
    
    row_count = len(df)
    logger.info(f"Converted DataFrame with {row_count} rows to Polars !")

    return pl.from_pandas(df)