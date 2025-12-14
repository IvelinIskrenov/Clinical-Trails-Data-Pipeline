import logging
from ETL.extract import extract_data, URL

def setup_logger():
    logger = logging.getLogger("ETL_Logger")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(ch)
    return logger

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("START TEST ...")

    data = extract_data()

    print("\nExtracted items:")
    print(data.head(30))
    
    logger.info("END TEST")