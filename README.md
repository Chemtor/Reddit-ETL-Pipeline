# Reddit ETL Pipeline

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)

A scalable ETL pipeline for extracting data from Reddit, transforming it, and loading it into a data warehouse for analysis.

## 📌 Overview

This pipeline extracts data from Reddit's API, processes it, and stores it in a structured format for analytics purposes.

## 🛠️ Architecture

```mermaid
graph TD
    A[Reddit API] -->|Extract| B(Raw JSON Data)
    B -->|Transform| C[Cleaned Data]
    C -->|Load| D[(Database PostGreSQL)]
    C -->|Load| E[Data Storage (Bucket B2)]
