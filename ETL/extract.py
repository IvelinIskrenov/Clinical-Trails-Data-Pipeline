import requests
from bs4 import BeautifulSoup
from typing import List
import logging
import pandas as pd

logger = logging.getLogger(__name__)

URL = "https://medicinraadet.dk/anbefalinger-og-vejledninger?page=1&order=updated%20desc&take=&currentpageid=1095&database=1095&secondary=1096&category=&archived=0&highlight=&q=&recommendation=1&recommendation=2&recommendation=8&period=0"
SOLUTION_TITLE_CLASS = 'database-item-title' 
NEXT_PAGE_CLASS = 'active item' 
SOLUTION_CLASS = 'database-item-header' 

def extract_solution_data(current_link) -> pd.DataFrame:
    """Extract the data for a single solution link"""
    
    logger.info(f" Start extracting the current solution link from: {current_link}")
    try:
        response = requests.get(current_link, timeout=15)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in HTTP request: {e}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser') #'lxml'

    #Find Active ingredient (generic name) & Trade name (brand name)
    h1_tag = soup.find('h1', class_ = 'ui header')
      
    if h1_tag and h1_tag.get_text(strip=True):
        target_tag = h1_tag.get_text(strip=True)
    else:
        all_font_tags = h1_tag.find('font').find('font')
        target_tag = all_font_tags[1]
    
    text_content = target_tag
    
    if '(' in text_content:
        active_ingredient  = text_content.split('(')[0].strip()
        trade_name = text_content.split('(')[1].split(')')[0].strip()
    else:
        active_ingredient = text_content
        trade_name = None
    
    # extract decision
    div_tag = soup.find('div', class_ = 'product-process')
    
    if div_tag and div_tag.get_text(strip=True):
        target_tag = div_tag.get_text(strip=True)
    else:
        all_font_tags = div_tag.find('font').find('font')
        target_tag = all_font_tags[1]
        
    decision = target_tag
    
    #extracting ATC code
    try:
        
        div_tag = soup.find('div', class_ = 'product-details product-content-limit-lg')
        product_detail_info = div_tag.find_all('div', 'product-detail')[1].find('div', 'product-detail-info')
        ATC_code = product_detail_info.get_text(strip = True)

    except Exception as e:
        print(f"Extract ATC error: {e.__class__.__name__}")
    
    # extract indication (Disease area)
    # for extract (Specific disease) switch to [4]
    try:
        #div_tag = soup.find('div', class_ = 'product-details product-content-limit-lg')
        product_detail_info = div_tag.find_all('div', 'product-detail')[2].find('div', 'product-detail-info') # switch to [4]
        indication = product_detail_info.get_text(strip = True)

    except Exception as e:
        print(f"Extract indication error: {e.__class__.__name__}")
    
    # extract decision_data
    try:
        decision_date = None
        div_tag = soup.find('div', class_ = 'product-block product-inset product-content-limit')
        if div_tag:
            product_detail_info = div_tag.find('p').find('i').get_text(strip=True).split(' ') 
            decision_date = product_detail_info[2] + ' ' + product_detail_info[3] + ' ' + product_detail_info[4]

    except Exception as e:
        print(f"Extract decision date error: {e.__class__.__name__}")

    dataframe_row = pd.DataFrame(
        [[decision, active_ingredient, trade_name, ATC_code, decision_date, indication]],
        columns=["decision", "active_ingredient", "trade_name", "ATC_code", "decision_date", "indication"]
    )
    
    return dataframe_row

def extract_next_page_href(url) -> str:
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

def extract_solution_hrefs(url) -> List[BeautifulSoup]:
    """Get the all links for all solutions in the current page"""
    
    logger.info(f" Start extracting links solutions from current page ...")
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status() 
    except requests.exceptions.RequestException as e:
        logger.error(f"Error in HTTP request: {e}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')

    solution_links = soup.find_all("div", class_ = SOLUTION_CLASS)
    if not solution_links:
        logger.info("No solution <a> tags found.")
        return []
    
    hrefs =[]
    for solution in solution_links:

        next_a = solution.find("a")
        if not next_a:
            logger.info("No href solution exists.")
            return None  
        href = next_a.get("href") 
        href = "https://medicinraadet.dk" + href
        hrefs.append(href) 
    
    logger.info(f"Solutions hrefs extracted for the current page - COUNT: '{len(hrefs)}'!")
    
    return hrefs

def extract_all_pages_links(start_url: str) -> list:
    """Walks through all pages starting from 'start_url', returns: list of pages URLs."""
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

    logger.info(f"Pages extracted - COUNT: '{len(pages)}'")
    
    return pages

def extract_all_solution_links(main_url) -> list[str]:
    """
    Collects and returns all solution links from every available page
    For each page it extracts all solution-specific hyperlinks using extract_solution_hrefs() and extract_all_pages_hrefs()
    Returns: list[str]: A list containing all unique solution URLs extracted from all pages.
    """
    all_solution_links = []
    
    pages = extract_all_pages_links(main_url)
    
    for page in pages:
        current_page_links = extract_solution_hrefs(page)
        all_solution_links.extend(current_page_links)
    
    logger.info(f"Extracted all solution links from the pages- COUNT: '{len(pages)}'")
        
    return all_solution_links    
    
def extract_data() -> pd.DataFrame:
    
    # indication col - (disease/condition the decision covers)
    columns = ['decision', 'active_ingredient', 'trade_name', 'ATC_code', 'decision_date', 'indication']
    data = pd.DataFrame(columns = columns) #empty
    
    
    result_links = extract_all_solution_links(URL)
    result_counts = 1
    for link in result_links:
        current_link_data = extract_solution_data(link) # output is a dataframe_row
        data = pd.concat([data, current_link_data], ignore_index=True)
        print(f"Reult link {result_counts} extracted !")
        result_counts = result_counts + 1
    
    return data
    