

import pandas as pd
import sqlite3


# 1. FILE PATHS


jobs_file = "data/processed/canada_data_jobs_clean.csv"

skills_file = "data/processed/noc_skill_profiles.csv"

skill_summary_file = "data/processed/skill_summary.csv"

technology_demand_file = "data/processed/technology_demand.csv"

technology_mentions_file = "data/processed/technology_mentions.csv"

database_file = "data/processed/job_market.db"


# 2. LOAD PROCESSED DATA


jobs = pd.read_csv(
    jobs_file
)

occupational_skills = pd.read_csv(
    skills_file
)

skill_summary = pd.read_csv(
    skill_summary_file
)

technology_demand = pd.read_csv(
    technology_demand_file
)

technology_mentions = pd.read_csv(
    technology_mentions_file
)


print("Files loaded successfully.")

print("Job postings:", jobs.shape)

print(
    "Occupational skills:",
    occupational_skills.shape
)

print(
    "Skill summary:",
    skill_summary.shape
)

print(
    "Technology demand:",
    technology_demand.shape
)

print(
    "Technology mentions:",
    technology_mentions.shape
)


# 3. CONNECT TO SQLITE


connection = sqlite3.connect(
    database_file
)

print(
    "\nConnected to SQLite database."
)


# 4. SAVE DATAFRAMES AS SQL TABLES


jobs.to_sql(
    "job_postings",
    connection,
    if_exists="replace",
    index=False
)

occupational_skills.to_sql(
    "occupational_skills",
    connection,
    if_exists="replace",
    index=False
)

skill_summary.to_sql(
    "skill_summary",
    connection,
    if_exists="replace",
    index=False
)

technology_demand.to_sql(
    "technology_demand",
    connection,
    if_exists="replace",
    index=False
)

technology_mentions.to_sql(
    "technology_mentions",
    connection,
    if_exists="replace",
    index=False
)


print(
    "\nTables saved successfully."
)


# 5. CHECK DATABASE TABLES


cursor = connection.cursor()

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type='table'
    ORDER BY name
    """
)

tables = cursor.fetchall()


print("\nTables in database:")

for table in tables:
    print(table[0])


# 6. VERIFY ROW COUNTS


cursor.execute(
    "SELECT COUNT(*) FROM job_postings"
)

job_count = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(*) FROM occupational_skills"
)

occupational_skill_count = (
    cursor.fetchone()[0]
)


cursor.execute(
    "SELECT COUNT(*) FROM skill_summary"
)

skill_count = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(*) FROM technology_demand"
)

technology_count = cursor.fetchone()[0]


cursor.execute(
    "SELECT COUNT(*) FROM technology_mentions"
)

technology_mention_count = (
    cursor.fetchone()[0]
)


print(
    "\nJob postings:",
    job_count
)

print(
    "Occupational skill profiles:",
    occupational_skill_count
)

print(
    "Skills in summary:",
    skill_count
)

print(
    "Technologies in demand table:",
    technology_count
)

print(
    "Technology mentions:",
    technology_mention_count
)


# 7. DISPLAY OCCUPATIONAL SKILL RANKINGS


cursor.execute(
    """
    SELECT
        Skill,
        Average_Rating
    FROM skill_summary
    ORDER BY Average_Rating DESC
    """
)

skill_results = cursor.fetchall()


print(
    "\nOccupational skill rankings:"
)

for row in skill_results:
    print(row)


# 8. DISPLAY TOP TECHNOLOGIES


cursor.execute(
    """
    SELECT
        Technology,
        Postings_Mentioning,
        Demand_Percentage
    FROM technology_demand
    ORDER BY
        Postings_Mentioning DESC,
        Technology ASC
    LIMIT 15
    """
)

technology_results = (
    cursor.fetchall()
)


print(
    "\nTop technologies:"
)

for row in technology_results:
    print(row)



# 9. CLOSE DATABASE


connection.close()


print(
    "\nDatabase connection closed."
)

print(
    "\nDatabase build complete."
)