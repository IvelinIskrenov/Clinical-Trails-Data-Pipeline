import pytest
import pandas as pd
import requests_mock
from bs4 import BeautifulSoup
from ETL.extract import ( 
    extract_solution_data,        
    extract_next_page_href,       
    extract_solution_hrefs,       
    extract_all_pages_links,      
    URL)


MOCK_SOLUTION_HTML = """
<html><body>
    <h1 class="ui header">Drug Name (Trade)</h1>
    <div class="product-process">Decision Value</div>
    <div class="product-details product-content-limit-lg">
        <div class="product-detail"></div> 
        <div class="product-detail"><div class="product-detail-info">A123</div></div>
        <div class="product-detail"><div class="product-detail-info">Indication Name</div></div> 
        <div></div>
    </div>
    <div class="product-block product-inset product-content-limit">
        <p><i>Some text 1 December 2002</i></p>
    </div>
</body></html>
"""

MOCK_PAGINATION_HTML = """
<html><body>
    <a class="active item" href="?page=1">1</a> 
    <a href="/anbefalinger?page=2">2</a> 
</body></html>
"""

MOCK_LINKS_HTML = """
<html><body>
    <div class="database-item-header"><a href="/sol/1">Title 1</a></div>
    <div class="database-item-header"><a href="/sol/2">Title 2</a></div>
</body></html>
"""

def test_extract_solution_data_success(requests_mock):
    mock_url = "https://medicinraadet.dk/mock-solution"
    requests_mock.get(mock_url, text=MOCK_SOLUTION_HTML)
    
    df_row = extract_solution_data(mock_url)
    
    assert isinstance(df_row, pd.DataFrame)
    assert len(df_row) == 1
    
    assert df_row.iloc[0]['active_ingredient'] == 'Drug Name'
    assert df_row.iloc[0]['trade_name'] == 'Trade'
    assert df_row.iloc[0]['decision'] == 'Decision Value'
    assert df_row.iloc[0]['ATC_code'] == 'A123'
    assert df_row.iloc[0]['indication'] == 'Indication Name'
    assert df_row.iloc[0]['decision_date'] == '1 December 2002'

def test_extract_solution_data_http_error(requests_mock):
    mock_url = "https://medicinraadet.dk/error"
    requests_mock.get(mock_url, status_code=404)
    
    result = extract_solution_data(mock_url)
    assert result == []

def test_extract_next_page_href_success(requests_mock):
    mock_base_url = "https://medicinraadet.dk/base?page=1"
    requests_mock.get(mock_base_url, text=MOCK_PAGINATION_HTML)
    
    result = extract_next_page_href(mock_base_url)
    assert result == "https://medicinraadet.dk/anbefalinger?page=2"


def test_extract_next_page_href_last_page(requests_mock):
    mock_url = "https://medicinraadet.dk/last-page"
    html_last_page = '<html><body><a class="active item" href="?page=10">10</a></body></html>'
    requests_mock.get(mock_url, text=html_last_page)
    
    result = extract_next_page_href(mock_url)
    assert result is None


def test_extract_solution_hrefs_success(requests_mock):
    mock_page_url = "https://medicinraadet.dk/page-with-links"
    requests_mock.get(mock_page_url, text=MOCK_LINKS_HTML)
    
    result = extract_solution_hrefs(mock_page_url)
    
    expected_links = [
        "https://medicinraadet.dk/sol/1",
        "https://medicinraadet.dk/sol/2",
    ]
    
    assert len(result) == 2
    assert result == expected_links

def test_extract_solution_hrefs_no_links(requests_mock):
    mock_page_url = "https://medicinraadet.dk/empty-page"
    requests_mock.get(mock_page_url, text="<html><body></body></html>")
    
    result = extract_solution_hrefs(mock_page_url)
    assert result == []


def test_extract_all_pages_links_multi_page(requests_mock):
    
    base_domain = "https://medicinraadet.dk"
    start_url = f"{base_domain}/page-1"

    requests_mock.get(start_url, text=MOCK_PAGINATION_HTML)

    html_page2 = '<html><body><a class="active item" href="?page=2">2</a></body></html>'
    requests_mock.get(f"{base_domain}/anbefalinger?page=2", text=html_page2)

    result = extract_all_pages_links(start_url)
    
    expected_pages = [
        start_url,
        f"{base_domain}/anbefalinger?page=2",
    ]
    
    assert result == expected_pages