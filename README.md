# ⚾ MLB World Series Data Explorer

This project is part of the final capstone for the Python course at [Code The Dream](https://codethedream.org). It demonstrates a complete end-to-end data pipeline — from web scraping and data cleaning to database integration and interactive dashboard visualization.

## Project Overview

This application scrapes historical baseball statistics from the [Baseball Almanac](https://www.baseball-almanac.com/yearmenu.shtml), cleans and stores the data into a SQLite database, and allows exploration via a command-line interface and a Streamlit-powered dashboard.


##  Project Components

### 1. Web Scraping Program
- Retrieves league leader stats (base on balls, batting, doubles, hits, home runs, on base, rbi, runs, stolen bases, triples), final standings, and team performances from the Baseball Almanac.
- Scrapes American and National Leagues historical data
- Technologies: `Selenium`, `CSV`, `Python`.

### 2. Data Cleaning
- Cleans raw scraped data using `Pandas`.
- Ensures consistency, removes non-numeric or malformed rows, and handles missing values.
- Exports structured and validated CSVs for each metric.

### 3. Database Import
- Creates a SQLite database (`mlb_cleaned.db`) and loads each cleaned CSV into a table.
- Handles type conversion, removes duplicates, and assigns proper table/column names.
- Uses `sqlite3` + `Pandas`.

### 4. Command-Line Interface
- Query the SQLite database using a terminal-based menu.
- Advanced statistical queries include:
  - Top 5 Stolen Bases (Year + League)
  - Top 10 Total Bases in a Year
  - Combined Doubles + Triples Leaders
  - All-Time Walk (Base on Balls) Leaders
  - Top 5 Combined Slugging Average + On-Base Percentage (OBP)
- Leverages `JOIN` operations and SQL sorting/filtering.

### 5. Streamlit Dashboard
- Interactive dashboard built with `Streamlit`, `Plotly`, and `Altair`.
- Features:
  - Year and league range sliders
  - Top 10 bar charts
  - Yearly line trends
  - Team share pie chart
  - Summary stats table

---

## Live Demo

[Streamlit App](https://mlb-capstone-project.streamlit.app/)

## Tech Stack

- **Python 3.12+**
- **Selenium**
- **SQLite3**
- **Pandas / NumPy**
- **Altair / Plotly / Streamlit**
- **CSV / Regex / OS / Dash (optional)**
