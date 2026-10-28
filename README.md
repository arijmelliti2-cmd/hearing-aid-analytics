# Hearing Aid Analytics

An end-to-end data engineering portfolio project that transforms synthetic hearing-aid device events into tested analytical models, product KPIs, and an interactive dashboard.

The project demonstrates how to build and orchestrate a data pipeline using **PostgreSQL, dbt, Apache Airflow, Docker, and Streamlit**, with automated validation through GitHub Actions.

> **Disclaimer:** All data is synthetic. This is a personal portfolio project, not a production system, medical device evaluation, or clinical recommendation.

## Project Overview

Hearing-aid devices generate data about their operating conditions, surrounding environments, and user feedback. This project demonstrates how such data can be transformed into structured analytics that help explore device usage and feedback patterns.

The pipeline processes event-level data, applies SQL transformations, validates data quality, and produces aggregated KPIs that can be explored through a dashboard.

### Key Features

- **Data transformation:** Build staging, intermediate, fact, dimension, and aggregated KPI models using dbt.
- **Data quality:** Validate identifiers, required fields, accepted values, and analytical constraints.
- **Workflow orchestration:** Schedule and monitor pipeline tasks using Apache Airflow.
- **Interactive analytics:** Explore device and activity metrics through a Streamlit dashboard.
- **Automated testing:** Run dbt validation and dashboard unit tests through GitHub Actions.
- **Reproducible environment:** Run the main services using Docker Compose.

## Architecture

```text
Synthetic CSV Events
        |
        v
    PostgreSQL
        |
        v
      dbt Seed
        |
        v
  Staging Models
        |
        v
Intermediate Models
        |
        v
 Fact + Dimensions
        |
        v
 Aggregated KPI Model
        |
        +----------------------+
        |                      |
        v                      v
 Streamlit Dashboard      Data Quality Tests
        ^
        |
  Apache Airflow
  Orchestration
```

Apache Airflow orchestrates the dbt workflow, including loading seed data, building analytical models, and generating documentation.

GitHub Actions provides separate automated workflows for dbt validation and dashboard unit tests.

## Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python, SQL, YAML |
| Data warehouse | PostgreSQL |
| Data transformation | dbt Core, dbt-postgres |
| Orchestration | Apache Airflow |
| Dashboard | Streamlit, Pandas, SQLAlchemy |
| Infrastructure | Docker, Docker Compose |
| Testing | dbt tests, pytest |
| CI/CD | GitHub Actions |
| Version control | Git, GitHub |

## Data Model

The project uses a synthetic CSV dataset containing hearing-aid event information.

### Source fields

- Event and user identifiers
- Event timestamps
- Environmental noise levels
- User activity
- Device battery percentage
- Volume level
- Noise-reduction settings
- User feedback ratings
- Device model

### Transformation layers

The dbt project separates transformations into logical layers:

- **Staging:** Standardize and prepare the source event data.
- **Intermediate:** Apply reusable transformations and derive analytical fields.
- **Fact model:** Represent hearing-aid events and connect them to device and activity dimensions.
- **Dimension models:** Organize device and activity attributes.
- **Aggregated KPI model:** Summarize metrics by device model and activity.

This layered structure improves maintainability, readability, and testability.

## Analytics and KPIs

The aggregated model groups events by device model and activity.

It calculates:

- Total event count
- Average feedback rating
- Number of low-feedback events
- Number of low-battery events
- Percentage of events recorded in loud environments
- Percentage of events combining loud environments with low feedback

These metrics are intended to demonstrate analytical modeling and aggregation techniques. Thresholds are illustrative and are not clinical guidance.

## Data Quality and Testing

The dbt project includes tests for:

- Unique event identifiers
- Required non-null fields
- Feedback ratings within the accepted range
- Valid battery and environmental noise ranges
- Uniqueness of device-model/activity KPI groups
- Valid KPI ranges

The dashboard also has pytest unit tests covering:

- Event-weighted average calculations
- Event-weighted percentage calculations
- Empty datasets
- Datasets with zero events

These tests help prevent calculation errors and support reliable changes to the project.

## Pipeline Orchestration

Apache Airflow orchestrates the analytical workflow through three tasks:

1. **Load seed data:** Load the synthetic CSV data into PostgreSQL using dbt.
2. **Build analytical models:** Execute dbt transformations and data quality tests.
3. **Generate documentation:** Generate dbt documentation for the project.

The DAG is configured to run daily at **06:00 Europe/Berlin time**. It also supports manual execution through the Airflow interface.

The local Airflow interface is available at:

`http://localhost:8081`

## Interactive Dashboard

The Streamlit dashboard reads the aggregated KPI model from PostgreSQL.

It provides:

- KPI summary cards
- Filtering by device model and activity
- Feedback comparisons across devices and activities
- Low-battery event counts
- Analysis of low feedback in loud environments
- A detailed view of aggregated results

Run the dashboard locally at:

`http://localhost:8501`

The dashboard uses event-weighted calculations when combining aggregated groups, so groups with different event counts are not treated as equally sized samples.

## Continuous Integration

Two GitHub Actions workflows validate the project.

### dbt CI

The dbt workflow:

- Starts a PostgreSQL service
- Installs dbt Core and dbt-postgres
- Configures the dbt profile
- Checks the database connection
- Loads the synthetic seed data
- Builds models and runs tests
- Generates dbt documentation

### Dashboard CI

The dashboard workflow:

- Sets up Python
- Installs dashboard dependencies
- Runs the dashboard unit tests

Both workflows run on pushes to `main` and pull requests targeting `main`.

## Getting Started

### Prerequisites

Install the following tools:

- Git
- Docker Desktop with Docker Compose
- Python 3.12, if you also want to run dbt directly from your local environment

### 1. Clone the repository

```bash
git clone https://github.com/arijmelliti2-cmd/hearing-aid-analytics.git
cd hearing-aid-analytics
```

### 2. Start the services

From the repository root, run:

```powershell
docker compose up --build -d
```

This builds and starts the configured PostgreSQL, Airflow, and dashboard services.

Check their status:

```powershell
docker compose ps
```

### 3. Open the applications

| Application | Local address |
|---|---|
| Streamlit dashboard | http://localhost:8501 |
| Apache Airflow | http://localhost:8081 |

Airflow's initial standalone administrator credentials are generated by Airflow. Retrieve them from the container logs or the password file inside the container:

```powershell
docker compose logs airflow
docker compose exec airflow cat /opt/airflow/standalone_admin_password.txt
```

The password file may not be available if your Airflow version or initialization process stores the credentials differently. Use the startup logs if necessary.

### 4. Run dbt locally (optional)

Create and activate a Python virtual environment from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dbt:

```powershell
python -m pip install dbt-core==1.8.8 dbt-postgres==1.8.2
```

Ensure that the local dbt profile exists at:

`%USERPROFILE%\.dbt\profiles.yml`

The profile must match the PostgreSQL configuration in your local Docker Compose setup.

Navigate to the dbt project:

```powershell
cd .\dbt_project\hearing_aid_analytics
```

Check the connection:

```powershell
dbt debug
```

Load the seed data and build the models:

```powershell
dbt seed
dbt build
```

Generate and serve the documentation:

```powershell
dbt docs generate
dbt docs serve
```

The documentation server normally runs at `http://localhost:8080`, provided that the port is available.

### 5. Run the dashboard unit tests

From the repository root, activate your virtual environment and install the dashboard dependencies:

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install -r dashboard\requirements.txt
python -m pip install pytest
```

Run the tests:

```powershell
$env:PYTHONPATH = "$PWD\dashboard"
python -m pytest dashboard\tests -v
```

## Example Results

The current synthetic dataset produces eight device-model/activity groups.

For example, the current data includes an average feedback rating of 2.50 for device model `HA_A` while commuting, based on two events. Both device models have an average rating of 4.50 while sitting in the sample.

These results demonstrate the pipeline and its calculations only. The dataset is deliberately small and does not support conclusions about real-world hearing-aid performance.

## Repository Structure

```text
hearing-aid-analytics/
├── .github/
│   └── workflows/
│       ├── dbt-ci.yml
│       └── dashboard-ci.yml
├── airflow/
│   └── profiles.yml
├── dashboard/
│   ├── app.py
│   ├── metrics.py
│   ├── requirements.txt
│   └── tests/
│       └── test_metrics.py
├── dags/
│   └── hearing_aid_pipeline.py
├── dbt_project/
│   └── hearing_aid_analytics/
│       ├── models/
│       ├── seeds/
│       ├── tests/
│       └── dbt_project.yml
├── Dockerfile.airflow
├── Dockerfile.dashboard
├── compose.yaml
└── README.md
```

The tree above highlights the main project components; additional dbt configuration files and models may exist within the dbt project directory.

## Future Improvements

Potential next steps include:

- Expand the synthetic dataset and introduce additional edge cases.
- Add incremental models and more advanced SQL transformations.
- Improve source freshness and data quality monitoring.
- Add more granular event-level analytics and dashboard drill-downs.
- Introduce separate development and production configurations.
- Improve secrets management through environment variables.
- Add integration tests for the complete pipeline.
- Explore additional orchestration and transformation patterns.

## Project Context

This repository is a personal portfolio project inspired by the hearing-aid analytics domain. It demonstrates practical data engineering concepts using synthetic data and locally runnable services.

It is intended to showcase skills in data modeling, pipeline orchestration, data quality, analytics, automated testing, and reproducible development environments.