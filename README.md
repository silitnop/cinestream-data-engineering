# CineStream — End-to-End Data Engineering Pipeline

## Project Overview

CineStream is a data engineering portfolio project designed to demonstrate a workflow for ingesting, validating, transforming, and analyzing movie-related data.

The project uses public MovieLens datasets for movie metadata and historical user ratings. Synthetic user profiles and watch-history events may be added in later stages to simulate streaming analytics.

**Important:** CineStream is a learning project. MovieLens ratings are historical rating records, not real-time streaming activity or actual subscriber data.

## Tech Stack

* **Python:** Data ingestion and validation
* **Pandas:** Data exploration and transformation
* **Jupyter Notebook:** Exploratory Data Analysis (EDA)
* **PostgreSQL:** Planned data storage
* **SQL / dbt:** Planned data modeling
* **Apache Airflow:** Planned pipeline orchestration
* **Power BI:** Planned dashboard
* **Docker:** Planned environment setup

## Dataset

The initial exploration uses these MovieLens files:

| File          | Description                                  |       Rows |
| ------------- | -------------------------------------------- | ---------: |
| `movies.csv`  | Movie IDs, titles, and genres                |     87,585 |
| `ratings.csv` | User IDs, movie IDs, ratings, and timestamps | 32,000,204 |

### Dataset Findings

* 87,585 unique movie IDs were found in `movies.csv`.
* 200,948 unique user IDs appear in `ratings.csv`.
* 84,432 unique movies received at least one rating.
* The observed rating range is 0.5 to 5.0.
* The mean rating is approximately 3.54, with a median of 3.5.
* Rating 4.0 is the most frequent rating, representing 26.15% of all ratings.
* The timestamp range is approximately 1995 to October 2023.

### Initial Data Quality Checks

The initial EDA found:

* No missing values in the inspected columns.
* No duplicate rows in `movies.csv` or `ratings.csv`.
* No duplicate `movieId` values in `movies.csv`.
* No duplicate `(userId, movieId)` pairs in the notebook checks.
* No ratings outside the expected 0.5–5.0 range.
* No rating records referencing unknown movie IDs.

These results describe the checks completed so far; additional validation will be performed as the pipeline evolves.

## Project Structure

```text
Cinestream/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   └── 01_data_exploration.ipynb
├── src/
│   └── ingestion/
│       └── inspect_data.py
├── sql/
├── tests/
├── dags/
├── requirements.txt
├── .gitignore
└── README.md
```

## Current Progress

* [x] Python virtual environment configured
* [x] Initial dependencies installed
* [x] Movie metadata explored
* [x] Rating dataset explored
* [x] Initial data quality checks performed
* [x] Python inspection script created
* [ ] PostgreSQL schema and loading process
* [ ] Data warehouse modeling
* [ ] Airflow orchestration
* [ ] Dashboard development
* [ ] Automated tests and final documentation

## Disclaimer

This project is an independent portfolio project for learning data engineering. MovieLens is the source of the public movie metadata and historical rating data. Any synthetic profiles or watch-history records will be identified as simulated data.
