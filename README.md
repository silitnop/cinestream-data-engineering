# 🎬 CineStream — End-to-End Data Engineering Pipeline

An end-to-end data engineering project that simulates a movie streaming platform to analyze movie performance and user viewing behavior using public movie datasets and synthetically generated streaming events.

## 📌 Project Overview

CineStream is a simulated streaming analytics platform designed to demonstrate how data engineers collect, process, validate, store, and transform data into actionable insights.

The project combines public movie metadata and rating datasets with synthetic user profiles and streaming activity. It aims to simulate a realistic data environment without using private customer data from real streaming platforms.

## 🎯 Objectives

* Build an automated ETL/ELT pipeline.
* Integrate public movie data with synthetic streaming events.
* Implement data validation and error handling.
* Store structured data in PostgreSQL.
* Design a data warehouse for analytical queries.
* Orchestrate workflows using Apache Airflow.
* Develop dashboards to analyze movie performance and viewing behavior.

## 🏗️ Planned Architecture

```text
Public Movie Data       Synthetic User Data
(MovieLens / TMDB)      (Python Generator)
        |                       |
        v                       v
   Data Ingestion         Event Generation
        |                       |
        +-----------+-----------+
                    |
                    v
               Apache Airflow
                    |
                    v
             Data Validation
                    |
                    v
             Python ETL / ELT
                    |
                    v
                PostgreSQL
                    |
                    v
              Data Warehouse
                    |
                    v
              SQL / dbt Models
                    |
                    v
             Power BI Dashboard
```

## 🗃️ Data Sources

### Public Data

* **MovieLens:** Movie metadata and historical user ratings.
* **TMDB API (optional):** Additional movie metadata, genres, release dates, and poster information.

### Synthetic Data

Python will generate fictional streaming-platform data, including:

* User profiles
* Subscription plans
* Watch history
* Watch duration
* Completion rates
* Streaming timestamps

**Note:** Synthetic users and streaming events do not represent actual customers or viewing activity from Netflix or any other real streaming service.

## 🧰 Technology Stack

| Technology     | Purpose                                        |
| -------------- | ---------------------------------------------- |
| Python         | Data ingestion, generation, and transformation |
| Pandas         | Data manipulation                              |
| NumPy          | Synthetic data generation                      |
| PostgreSQL     | Database and data warehouse storage            |
| Apache Airflow | Pipeline orchestration                         |
| SQL            | Data transformation and analytics              |
| Docker         | Reproducible environment                       |
| dbt            | SQL transformation and testing (planned)       |
| Power BI       | Data visualization (planned)                   |
| Git & GitHub   | Version control and documentation              |

## 📊 Planned Data Model

### Source Tables

* `movies`
* `ratings`
* `users`
* `watch_history`

### Data Warehouse

**Fact tables**

* `fact_watch`
* `fact_rating`

**Dimension tables**

* `dim_user`
* `dim_movie`
* `dim_genre`
* `dim_date`

The warehouse will use dimensional modeling principles to support analytical queries and reporting.

## 📈 Business Questions

The project aims to answer questions such as:

* Which movies and genres receive the most viewing activity?
* What is the average watch duration per user?
* Which movies have the highest completion rates?
* How does viewing behavior differ across subscription plans?
* Which countries generate the most viewing hours?
* How does viewing activity change over time?

## ⚙️ Planned Engineering Features

* Scheduled data ingestion
* Synthetic streaming event generation
* Data cleaning and schema validation
* Duplicate detection
* Referential integrity checks
* Incremental data loading
* Pipeline logging and error handling
* Data warehouse modeling
* Automated data quality tests
* Containerized development environment

## 🗺️ Development Roadmap

* [ ] Select and document public movie datasets.
* [ ] Design the database schema.
* [ ] Build a synthetic user and streaming event generator.
* [ ] Implement Python-based data ingestion and transformation.
* [ ] Load data into PostgreSQL.
* [ ] Add data quality checks.
* [ ] Orchestrate workflows using Apache Airflow.
* [ ] Implement incremental loading.
* [ ] Build dimensional warehouse models.
* [ ] Develop analytical SQL queries.
* [ ] Create a Power BI dashboard.
* [ ] Containerize the environment using Docker.
* [ ] Add automated tests and usage documentation.

## 🔒 Data Privacy and Limitations

This project uses public datasets and synthetic streaming activity. It does not use or claim access to proprietary streaming-platform customer data.

Synthetic data is intended for engineering demonstrations and controlled analytical experiments. Results derived from synthetic activity should not be interpreted as actual customer behavior.

## 📌 Project Status

**Status: In Development**

This project is being developed as a portfolio project to demonstrate practical data engineering skills, from data ingestion and orchestration to data warehousing and analytics.

## 📄 Data Attribution

Public datasets and APIs are subject to their respective licenses, attribution requirements, and terms of use. Specific sources and applicable licenses will be documented as they are integrated into the project.
