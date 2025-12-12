import requests
from bs4 import BeautifulSoup
from typing import List
import logging

logger = logging.getLogger('ETL_Logger') 

URL = "https://medicinraadet.dk/anbefalinger-og-vejledninger?page=1&order=updated%20desc&take=&currentpageid=1095&database=1095&secondary=1096&category=&archived=0&highlight=&q=&recommendation=1&recommendation=2&recommendation=8&period=0"
SOLUTION_TITLE_CLASS = 'database-item-title' 
NEXT_PAGE_CLASS = 'active item' # maybe search active-item then go to sibiling to get the next page ?
SOLUTION_CLASS = 'database-item-category'

def extract_page(url: str = URL) -> List[BeautifulSoup]:
    """Extracting the title"""
    logger.info(f" Start extracting from: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in HTTP request: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    rows_title = soup.find_all('h3', class_=SOLUTION_TITLE_CLASS)
    rows_page = soup.find_all()
    
    if not rows_title:
        logger.error(f"There is no elements '{SOLUTION_TITLE_CLASS}'. Diffrent html structure.")

    logger.info(f"Successfully extracted {len(rows_title)} records for class '{SOLUTION_TITLE_CLASS}'")
    print("___________________________")
    print(type(rows_title))
    print("___________________________")
    return rows_title

# should give the next page, so we need add the numer of the current page (Chech if we get the next page or we are looping on the first 2 pages)
def extract_next_page_href(url, page) -> str:
    """Returning the next page href"""
    
    logger.info(f" Start extracting the next page from: {url}")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in HTTP request: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    active = soup.find("a", class_ = NEXT_PAGE_CLASS)
    if not active:
        logger.error("Active page <a> not found.")
        return None

    next_a = active.find_next_sibling("a")
    if not next_a:
        logger.info("No next page exists (we are on the last page).")
        return None

    href = next_a.get("href")
    logger.info(f"Next page href: {href}")
    
    href = "https://medicinraadet.dk" + href
    
    return href

# should test
def extract_solution_hrefs(url) -> List[BeautifulSoup]:
    """Get the all hrefs for all solutions in the current page"""
    
    logger.info(f" Start extracting hrefs solutions from current page ...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in HTTP request: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    solutions = soup.find("a", class_ = SOLUTION_CLASS)
    
    hrefs =[]
    
    for solution in solutions:
        if not solution:
            logger.error("Active page <a> not found.")
            return None

        next_a = solution.find_next_sibling("a")
        if not next_a:
            logger.info("No href solution exists.")
            return None  
        href = next_a.get("href") 
        href = "https://medicinraadet.dk" + href
        hrefs.insert(href) 
    
    logger.info(f"Solutions hrefs extracted !")
    
    return hrefs

def extract_all_pages_hrefs(start_url: str) -> list:
    """Walks through all pages starting from 'start_url', returns: list of page URLs."""
    pages = []
    current_url = start_url

    while True:
        pages.append(current_url)
        logger.info(f"Collected page: {current_url}")

        next_url = extract_next_page_href(current_url)

        if not next_url:
            logger.info("No more pages. Stopping.")
            break

        current_url = next_url

    return pages
    
def extract_data() -> List[BeautifulSoup]:
    data = None
    """
    for page in pages:
        for title in titles:
            extract_title()
    
    """
    pages = extract_all_pages_hrefs(URL)
    
    return data
    