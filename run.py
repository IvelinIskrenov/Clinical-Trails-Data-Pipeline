import logging
from ETL import extract_data, extract_data_parallel, transform, load_to_polars, URL
import pandas as pd

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(ch)
    return logger

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("START TEST ...")

    #ETL
    data = extract_data_parallel()
    transformed_data = transform(data)
    data_polars = load_to_polars(transformed_data)

    #print("\nExtracted items:")
    #print(data.head(250))
    
    logger.info("END TEST")