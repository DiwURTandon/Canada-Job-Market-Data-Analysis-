import sqlite3


connection = sqlite3.connect(
    "data/processed/job_market.db"
)

cursor = connection.cursor()


# 1. TOTAL JOB POSTINGS


cursor.execute("""
SELECT COUNT(*)
FROM job_postings
""")

print(
    "\nTotal valid salary job postings:",
    cursor.fetchone()[0]
)


# 2. JOB POSTINGS BY PROVINCE


cursor.execute("""
SELECT
    Province_Territory,
    COUNT(*) AS Job_Count
FROM job_postings
GROUP BY Province_Territory
ORDER BY Job_Count DESC
""")

print("\nJOB POSTINGS BY PROVINCE")

for row in cursor.fetchall():
    print(row)


# 3. JOB POSTINGS BY MONTH


cursor.execute("""
SELECT
    Month,
    COUNT(*) AS Job_Count
FROM job_postings
GROUP BY Month
ORDER BY Month
""")

print("\nJOB POSTINGS BY MONTH")

for row in cursor.fetchall():
    print(row)


# 4. MOST COMMON JOB TITLES


cursor.execute("""
SELECT
    Job_Title,
    COUNT(*) AS Job_Count
FROM job_postings
GROUP BY Job_Title
ORDER BY Job_Count DESC
LIMIT 10
""")

print("\nTOP JOB TITLES")

for row in cursor.fetchall():
    print(row)


# 5. AVERAGE SALARY BY JOB TITLE


cursor.execute("""
SELECT
    Job_Title,
    COUNT(*) AS Job_Count,
    ROUND(AVG(Estimated_Annual_Mid), 2) AS Average_Salary
FROM job_postings
WHERE Estimated_Annual_Mid IS NOT NULL
GROUP BY Job_Title
HAVING COUNT(*) >= 2
ORDER BY Average_Salary DESC
""")

print("\nAVERAGE SALARY BY JOB TITLE")

for row in cursor.fetchall():
    print(row)


# 6. AVERAGE SALARY BY PROVINCE


cursor.execute("""
SELECT
    Province_Territory,
    COUNT(*) AS Job_Count,
    ROUND(AVG(Estimated_Annual_Mid), 2) AS Average_Salary
FROM job_postings
WHERE Estimated_Annual_Mid IS NOT NULL
GROUP BY Province_Territory
ORDER BY Average_Salary DESC
""")

print("\nAVERAGE SALARY BY PROVINCE")

for row in cursor.fetchall():
    print(row)


# 7. OCCUPATIONAL SKILL RANKINGS


cursor.execute("""
SELECT
    Skill,
    ROUND(Average_Rating, 2) AS Average_Rating
FROM skill_summary
ORDER BY Average_Rating DESC
""")

print("\nOCCUPATIONAL SKILL RANKINGS")

for row in cursor.fetchall():
    print(row)



# CLOSE DATABASE


connection.close()

print("\nAnalysis complete.")