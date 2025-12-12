import logging
from ETL.extract import extract_all_solution_links, URL

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

    data = extract_all_solution_links(URL)

    #print("\nExtracted items:")
    #for d in data:
    #    print(d)
    #    print(" ")
    
    logger.info("END TEST")