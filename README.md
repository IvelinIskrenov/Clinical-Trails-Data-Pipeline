# Clinical-Trails-Data-Pipeline

## This project implements an ETL (Extract, Transform, Load) process designed to extract, filter, and load data.

### Architecture and File Structure

run.py Sets up logging and starts the execution of the entire ETL process.
ETL -> extract.py Extracts data from the website.
ETL -> transform.py Filters the extracted data.
ETL -> load.py Loads the final data into the Polars/Pandas DataFrame.
tests -> test_extract.py, test_transform.py, test_load.py - tests the ETL module

### Extract Approach

Collect all URLs of the results pages (extract_all_pages_links).

Extract all individual solution links from those pages (extract_all_solution_links).

Extract detailed data from each link (extract_solution_data).

Parallelization: Uses concurrent.futures.ThreadPoolExecutor (extract_data_parallel()) to execute multiple requests simultaneously. This significantly speeds up the data extraction process by reducing the time spent waiting for responses from the server.

Parsing Errors: A Logger (logger.error) is used to record any errors while the process continues. 
Logging: Detailed logging at each stage (logger.info for start/end, logger.error for errors) provides observability and makes it easier to debug scraping issues.

### Transform Approach
Filter by Solution: The transform() function filters the DataFrame to include only solutions with statuses "Recommended" or "Partially recommended".

### Load Approach
The data that comes as a Pandas DataFrame is converted to a Polars DataFrame (load_to_polars()).

# Installation and requirements
## 1. Clone the Repository
### in bash: git clone https://github.com/IvelinIskrenov/Clinical-Trails-Data-Pipeline.git

## 2. Create virtual ENV
### in bash: python -m venv venv
###          .\venv\Scripts\activate    (for windows)
###          source venv/bin/activate   (for Linux)

## 3. Install requiremnts.txt
### in bash: pip install -r requirements.txt

## 4. To run the ETL Pipe
### i bash: python run.py 

# Unit tests

## To run the unit test 
### 1. go to project etl folder and open bash
### in the console run: python -m pytest/test_extract.py