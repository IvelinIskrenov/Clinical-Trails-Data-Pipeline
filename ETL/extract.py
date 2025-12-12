import requests
from bs4 import BeautifulSoup
from typing import List
import logging

logger = logging.getLogger('ETL_Logger') 

URL = "https://medicinraadet.dk/anbefalinger-og-vejledninger?page=1&order=updated%20desc&take=&currentpageid=1095&database=1095&secondary=1096&category=&archived=0&highlight=&q=&recommendation=1&recommendation=2&recommendation=8&period=0"
PRODUCT_CLASS = 'database-item-title' 
NEXT_PAGE_CLASS= 'item' # maybe search active-item then go to sibiling to get the next page ?


def extract_data(url: str = URL) -> List[BeautifulSoup]:

    logger.info(f" Start extracting from: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in HTTP request: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    rows = soup.find_all('h3', class_=PRODUCT_CLASS)
    
    if not rows:
        logger.error(f"There is no elements '{PRODUCT_CLASS}'. Diffrent html structure.")

    logger.info(f"Successfully extracted {len(rows)} records for class '{PRODUCT_CLASS}'")
    return rows

def extract_next_page(url) -> BeautifulSoup:
    logger.info(f" Start extracting the next page from: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in HTTP request: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    rows = soup.find_all('a', class_=NEXT_PAGE_CLASS)
    
    if not rows:
        logger.error(f"There is no elements '{NEXT_PAGE_CLASS}'. Diffrent html structure.")

    logger.info(f"Successfully extracted {len(rows)} records for class '{NEXT_PAGE_CLASS}'")
    return rows