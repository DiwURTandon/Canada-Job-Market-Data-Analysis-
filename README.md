# Canadian Job Market Analysis

## Overview

This project analyzes real Canadian job posting data to explore demand for data analytics and data science roles across Canada.

The analysis focuses on job posting volume, geographic demand, salary patterns, occupational skills, and employer technology requirements. The final results are presented through an interactive Streamlit dashboard.

The goal of the project is to provide an evidence-based view of what the Canadian data job market expects from candidates rather than relying on general career advice.

---

## Objective

The main objectives of this project are to:

- Collect and analyze Canadian job posting data for data-related careers.
- Identify which provinces and cities have the highest job demand.
- Analyze salary patterns across job titles and regions.
- Study occupational skills required for data-related careers.
- Identify technologies and programming tools mentioned in verified Job Bank postings.
- Store and query the cleaned data using SQLite and SQL.
- Present the findings through an interactive Streamlit dashboard.

---

## Data Sources

### Government of Canada Job Bank

Monthly Job Bank open-data files from:

- March 2026
- April 2026
- May 2026
- June 2026
- July 2026

These datasets were used for:

- Job posting volume
- Province and city analysis
- Job title analysis
- Salary analysis
- Vacancy counts

### Government of Canada OaSIS

OaSIS occupational data was linked to Job Bank postings using NOC 2021 codes.

This dataset was used to analyze occupational competencies such as:

- Problem Solving
- Digital Literacy
- Critical Thinking
- Systems Analysis
- Numeracy
- Decision Making
- Reading Comprehension
- Writing
- Troubleshooting
- Time Management

---

## Technologies Used

- Python
- pandas
- SQLite
- SQL
- Streamlit
- Git
- GitHub
- Jupyter Notebook

---

## Project Workflow

### 1. Data Collection

Five months of Government of Canada Job Bank open-data files were collected.

### 2. Data Cleaning

The datasets were filtered for data-related roles including:

- Data Scientist
- Data Analyst
- Business Data Analyst
- Business Intelligence roles
- Data Analytics Specialist
- Data Quality Analyst

Missing values were reviewed, date formats were standardized, and useful columns were selected for further analysis.

### 3. Salary Standardization

Salary information was provided using hourly, yearly, and bi-weekly formats.

To make salary values comparable:

- Hourly salaries were converted using 40 hours per week × 52 weeks per year.
- Bi-weekly salaries were converted using 26 pay periods per year.

Clearly malformed salary records were excluded from salary analysis.

### 4. SQLite and SQL Analysis

The cleaned dataset was stored in a SQLite database.

SQL queries were used to analyze:

- Job postings by province
- Job postings by month
- Most common job titles
- Average salary by job title
- Average salary by province
- Occupational skills
- Technology demand

### 5. Occupational Skills Analysis

OaSIS occupational profiles were matched to Job Bank postings through NOC 2021 codes.

The strongest posting-weighted occupational skills were:

- Problem Solving: 4.83 / 5
- Digital Literacy: 4.67 / 5
- Critical Thinking: 4.67 / 5
- Systems Analysis: 4.67 / 5
- Numeracy: 4.42 / 5

### 6. Technology Demand Analysis

The monthly Job Bank CSV files do not include complete job requirement text.

To analyze technologies, a subset of direct Job Bank postings was matched to archived Job Bank information.

Technology requirements were successfully verified for a smaller sample of direct Job Bank postings.

Technologies identified included:

- Python
- SQL
- MySQL
- AWS
- C++
- Java
- Linux
- Machine Learning
- Data Warehouse
- Database Software
- Programming Software

Technology demand percentages are based only on the verified direct Job Bank sample and should not be interpreted as representing every posting in the full dataset.

### 7. Dashboard Development

An interactive Streamlit dashboard was created to visualize:

- Total job postings
- Reported vacancies
- Job demand by province
- Monthly posting trends
- Most common job titles
- Salary by job title
- Salary by province
- Occupational skills
- Technology demand
- Individual job posting data

The dashboard also includes filters for province, month, and job title.

---

## Key Findings

### 1. Ontario had the highest job demand

Ontario accounted for 131 of the 231 salary-valid job postings analyzed, making it the strongest province for data-related opportunities in the dataset.

### 2. Data Scientist was the most common job title

There were 96 Data Scientist postings, followed by 68 Data Analyst - Informatics and Systems postings.

### 3. Data Scientist salaries were relatively high

Data Scientist postings had an estimated average annual salary of approximately $102,762.

Lead Data Scientist roles had the highest average salary among job titles represented by at least two postings, at approximately $137,800.

### 4. Problem solving was the strongest occupational competency

Problem Solving had the highest OaSIS posting-weighted rating at approximately 4.83 out of 5.

Digital Literacy, Critical Thinking, and Systems Analysis each had an average rating of approximately 4.67.

### 5. Python appeared frequently in the verified technology sample

Python appeared in 4 of 19 verified direct Job Bank postings used for the technology analysis, representing approximately 21.05% of the verified sample.

SQL appeared in 3 postings, while technologies such as AWS, C++, Java, MySQL, Linux, and Machine Learning were also identified.

---

## Project Structure

```text
CA JOB Market/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── canada_data_jobs_clean.csv
│       ├── jobs_with_skills.csv
│       ├── job_market.db
│       ├── noc_skill_profiles.csv
│       ├── skill_summary.csv
│       ├── technology_collection.csv
│       ├── technology_demand.csv
│       ├── technology_mentions.csv
│       └── verified_technology_jobs.csv
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── src/
│   ├── database.py
│   ├── sql_analysis.py
│   └── test_setup.py
│
├── .gitignore
├── requirements.txt
└── README.md