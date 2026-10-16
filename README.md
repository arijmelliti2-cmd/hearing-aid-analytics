
# Hearing Aid Analytics

## Overview

A personal data engineering portfolio project that transforms synthetic
hearing-aid device events into analytical models and product KPIs.

The project demonstrates data ingestion, SQL transformations, data quality
testing, and analytics using PostgreSQL and dbt.

**Note:** All data is synthetic. This is a personal portfolio project, not
a production system or a clinical evaluation.

## Architecture

CSV seed data
    -> PostgreSQL
    -> dbt staging
    -> dbt intermediate transformations
    -> fact table
    -> aggregated analytics KPIs

## Technology Stack

- Python virtual environment
- Docker and Docker Compose
- PostgreSQL
- dbt Core
- dbt-postgres
- SQL and YAML

## Data

The synthetic dataset includes:

- Device and user identifiers
- Event timestamps
- Environmental noise levels
- User activity
- Battery percentage
- Volume and noise-reduction settings
- Feedback ratings
- Device model

## Analytics

The KPI model groups events by device model and activity.

It calculates:

- Total events
- Average feedback rating
- Number of low-feedback events
- Number of low-battery events
- Percentage of events in loud environments
- Percentage of events with low feedback in loud environments

## Data Quality

The project includes tests for:

- Unique event identifiers
- Required non-null fields
- Feedback ratings between 1 and 5
- Valid battery and environmental noise ranges
- Unique device-model/activity groups in the KPI model
- Valid KPI ranges

## Run Locally

Start PostgreSQL from the project root:

    docker compose up -d

Activate the Python environment in PowerShell:

    .\.venv\Scripts\Activate.ps1

Navigate to the dbt project:

    cd .\dbt_project\hearing_aid_analytics

Check the connection:

    dbt debug

Build the project and run tests:

    dbt build

Generate and serve documentation:

    dbt docs generate
    dbt docs serve

## Example Results

The current synthetic dataset produces 8 device-model/activity groups.

Example observations include an average feedback rating of 2.50 for
HA_A while commuting, based on 2 events, and 4.50 for both device
models while sitting.

These small synthetic samples demonstrate the pipeline only; they do
not establish real-world device performance.

## Future Improvements

- Add larger and more realistic synthetic datasets
- Add more advanced SQL transformations and KPI tests
- Add automated pipeline orchestration with Airflow
- Add a dashboard for KPI exploration
- Add CI checks for dbt builds and tests
