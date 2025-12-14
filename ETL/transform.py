import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    
    initial_rows = len(df)
    logger.info(f"Starting transformation. Initial row count: {initial_rows}")
    
    # filter the decisions only (Recommended and Partially recommended)    
    allowed_decisions = ["Recommended", "Partially recommended", "Anbefalet", "Delvist anbefalet"]
    data_filtered = df[df["decision"].isin(allowed_decisions)]
    
    filtered_rows = len(data_filtered)
    logger.info(f"Rows after filtering by decision ({allowed_decisions}): {filtered_rows}")
    logger.info(f"Dropped {initial_rows - filtered_rows} rows during transformation")
    
    return data_filtered