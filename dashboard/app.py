import streamlit as st
import pandas as pd
import sqlite3


# PAGE CONFIGURATION


st.set_page_config(
    page_title="Canadian Data Job Market",
    page_icon="🇨🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# DESIGN SYSTEM


PRIMARY = "#1B3B6F"
ACCENT = "#D62828"
BG_PAGE = "#F5F7FA"
BG_CARD = "#FFFFFF"
TEXT_MUTED = "#5B6472"
BORDER = "#E4E8EE"


def render_html(content: str) -> None:
    """
    Render an HTML fragment safely.

    st.markdown() treats any line indented 4+ spaces as a Markdown
    code block, which breaks HTML rendering when the source string
    is written with nested Python indentation for readability. This
    strips leading whitespace from every line before handing the
    string to st.markdown(), so the HTML always renders correctly
    regardless of how it's indented in the source file.
    """
    lines = [line.strip() for line in content.strip("\n").splitlines()]
    st.markdown("\n".join(lines), unsafe_allow_html=True)


def render_html_sidebar(content: str) -> None:
    """Same as render_html(), but renders into the sidebar."""
    lines = [line.strip() for line in content.strip("\n").splitlines()]
    st.sidebar.markdown("\n".join(lines), unsafe_allow_html=True)


render_html(
    f"""
    <style>

        html, body, [class*="css"] {{
            font-family: -apple-system, BlinkMacSystemFont,
                "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}

        .stApp {{
            background-color: {BG_PAGE};
        }}

        /*  HERO  */

        .hero {{
            background: linear-gradient(135deg, {PRIMARY} 0%, #26518C 100%);
            padding: 2.4rem 2.6rem;
            border-radius: 14px;
            color: white;
            margin-bottom: 1.6rem;
            box-shadow: 0 8px 24px rgba(27, 59, 111, 0.18);
        }}

        .hero h1 {{
            font-size: 2rem;
            font-weight: 800;
            margin: 0 0 0.5rem 0;
            letter-spacing: -0.01em;
        }}

        .hero p {{
            font-size: 1.02rem;
            opacity: 0.92;
            margin: 0;
            max-width: 850px;
            line-height: 1.5;
        }}

        .hero .badge {{
            display: inline-block;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.3);
            padding: 0.2rem 0.7rem;
            border-radius: 999px;
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.03em;
            margin-bottom: 0.9rem;
        }}

        /* SECTION HEADERS  */

        .section-title {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {PRIMARY};
            margin-bottom: 0.2rem;
        }}

        .section-sub {{
            color: {TEXT_MUTED};
            font-size: 0.92rem;
            margin-bottom: 1rem;
        }}

        .subsection-title {{
            font-size: 1.02rem;
            font-weight: 700;
            color: {PRIMARY};
            margin: 0 0 0.7rem 0;
        }}

        /*  KPI CARDS  */

        .kpi-card {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 1.15rem 1.3rem;
            box-shadow: 0 2px 8px rgba(20,30,60,0.04);
            height: 100%;
        }}

        .kpi-label {{
            font-size: 0.78rem;
            font-weight: 600;
            color: {TEXT_MUTED};
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 0.35rem;
        }}

        .kpi-value {{
            font-size: 1.9rem;
            font-weight: 800;
            color: {PRIMARY};
            line-height: 1.1;
        }}

        /* CONTENT CARDS  */

        .content-card {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 1.3rem 1.4rem 0.9rem 1.4rem;
            box-shadow: 0 2px 8px rgba(20,30,60,0.04);
            margin-bottom: 1.6rem;
        }}

        /*  MISC */

        .caption-note {{
            color: {TEXT_MUTED};
            font-size: 0.85rem;
        }}

        section[data-testid="stSidebar"] {{
            background-color: {PRIMARY};
        }}

        section[data-testid="stSidebar"] * {{
            color: #EAEFF7 !important;
        }}

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        hr {{
            border: none;
            border-top: 1px solid {BORDER};
            margin: 1.8rem 0;
        }}

        [data-testid="stDataFrame"] {{
            border-radius: 8px;
            overflow: hidden;
        }}

        [data-testid="stMetric"] {{
            background: {BG_CARD};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 0.9rem 1.1rem;
            box-shadow: 0 2px 8px rgba(20,30,60,0.04);
        }}

        [data-testid="stMetricLabel"] {{
            color: {TEXT_MUTED};
        }}

        [data-testid="stMetricValue"] {{
            color: {PRIMARY};
        }}

    </style>
    """
)


CHART_COLOR = PRIMARY


# LOAD DATA


@st.cache_data
def load_data():

    connection = sqlite3.connect(
        "data/processed/job_market.db"
    )

    jobs = pd.read_sql_query(
        """
        SELECT *
        FROM job_postings
        """,
        connection
    )

    skills = pd.read_sql_query(
        """
        SELECT *
        FROM skill_summary
        """,
        connection
    )

    technology_demand = pd.read_sql_query(
        """
        SELECT *
        FROM technology_demand
        """,
        connection
    )

    technology_mentions = pd.read_sql_query(
        """
        SELECT *
        FROM technology_mentions
        """,
        connection
    )

    connection.close()

    verified_technology_jobs = pd.read_csv(
        "data/processed/verified_technology_jobs.csv"
    )

    return (
        jobs,
        skills,
        technology_demand,
        technology_mentions,
        verified_technology_jobs
    )


(
    jobs,
    skills,
    technology_demand,
    technology_mentions,
    verified_technology_jobs
) = load_data()


# DATES


technology_mentions["Posting_Date"] = pd.to_datetime(
    technology_mentions["Posting_Date"]
)

verified_technology_jobs["Posting_Date"] = pd.to_datetime(
    verified_technology_jobs["Posting_Date"]
)

technology_mentions["Month"] = (
    technology_mentions["Posting_Date"].dt.to_period("M").astype(str)
)

verified_technology_jobs["Month"] = (
    verified_technology_jobs["Posting_Date"].dt.to_period("M").astype(str)
)


# HERO


render_html(
    """
    <div class="hero">
        <div class="badge">MARCH – JULY 2026</div>
        <h1>🇨🇦 Canadian Data Job Market Dashboard</h1>
        <p>
            Explore Canadian data analytics and data science job postings
            through job demand, salary trends, regional distribution,
            occupational competencies, and verified employer technology
            requirements.
        </p>
    </div>
    """
)


# SIDEBAR FILTERS


st.sidebar.markdown("### 🔎 Filter Job Postings")

render_html_sidebar(
    """
    <div style="opacity:0.75; font-size:0.85rem; margin-bottom:1rem;">
        Refine the dashboard using the filters below.
    </div>
    """
)

province_options = sorted(
    jobs["Province_Territory"].dropna().unique()
)

selected_provinces = st.sidebar.multiselect(
    "Province / Territory",
    province_options,
    default=province_options
)

month_options = sorted(
    jobs["Month"].dropna().unique()
)

selected_months = st.sidebar.multiselect(
    "Month",
    month_options,
    default=month_options
)

job_title_options = sorted(
    jobs["Job_Title"].dropna().unique()
)

selected_titles = st.sidebar.multiselect(
    "Job Title",
    job_title_options,
    default=job_title_options
)

render_html_sidebar(
    "<hr style='border-color: rgba(255,255,255,0.2);'>"
)

render_html_sidebar(
    """
    <div style="opacity:0.8; font-size:0.85rem; line-height:1.6;">
        <b style="opacity:0.95;">Sources</b><br>
        Government of Canada Job Bank<br>
        Government of Canada OaSIS
    </div>
    """
)


# APPLY MAIN JOB FILTERS


filtered_jobs = jobs[
    jobs["Province_Territory"].isin(selected_provinces)
    &
    jobs["Month"].isin(selected_months)
    &
    jobs["Job_Title"].isin(selected_titles)
].copy()


# MARKET OVERVIEW


render_html('<div class="section-title">📊 Market Overview</div>')
render_html(
    '<div class="section-sub">'
    'Key figures for the currently selected job-market filters.'
    '</div>'
)

total_jobs = len(filtered_jobs)
total_vacancies = filtered_jobs["Vacancy_Count"].sum()
province_count = filtered_jobs["Province_Territory"].nunique()
average_salary = filtered_jobs["Estimated_Annual_Mid"].mean()

kpi_values = [
    ("Job Postings", f"{total_jobs:,}"),
    ("Reported Vacancies", f"{total_vacancies:,.0f}"),
    ("Provinces / Territories", f"{province_count}"),
    (
        "Average Estimated Salary",
        f"${average_salary:,.0f}" if pd.notna(average_salary) else "N/A"
    )
]

kpi_cols = st.columns(4)

for col, (label, value) in zip(kpi_cols, kpi_values):
    with col:
        render_html(
            f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """
        )

render_html(
    """
    <div class="caption-note" style="margin-top:0.7rem;">
        Dashboard values update automatically when filters are changed.
    </div>
    """
)

render_html("<hr>")


# JOB DEMAND BY PROVINCE


render_html('<div class="section-title">🗺️ Job Demand by Province / Territory</div>')

province_jobs = (
    filtered_jobs["Province_Territory"]
    .value_counts()
    .sort_values()
    .reset_index()
)
province_jobs.columns = ["Province / Territory", "Job Postings"]

with st.container():
    render_html('<div class="content-card">')

    st.bar_chart(
        province_jobs,
        x="Province / Territory",
        y="Job Postings",
        horizontal=True,
        color=CHART_COLOR
    )

    render_html("</div>")


# JOB POSTINGS OVER TIME


render_html('<div class="section-title">📈 Job Postings Over Time</div>')

monthly_jobs = (
    filtered_jobs["Month"]
    .value_counts()
    .sort_index()
    .reset_index()
)
monthly_jobs.columns = ["Month", "Job Postings"]

with st.container():
    render_html('<div class="content-card">')

    st.line_chart(
        monthly_jobs,
        x="Month",
        y="Job Postings",
        color=CHART_COLOR
    )

    render_html("</div>")


# TOP JOB TITLES


render_html('<div class="section-title">💼 Most Common Job Titles</div>')

top_titles = (
    filtered_jobs["Job_Title"]
    .value_counts()
    .head(10)
    .sort_values()
    .reset_index()
)
top_titles.columns = ["Job Title", "Job Postings"]

with st.container():
    render_html('<div class="content-card">')

    st.bar_chart(
        top_titles,
        x="Job Title",
        y="Job Postings",
        horizontal=True,
        color=CHART_COLOR
    )

    render_html("</div>")


# SALARY ANALYSIS


render_html('<div class="section-title">💰 Salary Analysis</div>')

salary_by_title = (
    filtered_jobs
    .dropna(subset=["Estimated_Annual_Mid"])
    .groupby("Job_Title")
    .agg(
        Job_Count=("Job_Title", "size"),
        Average_Salary=("Estimated_Annual_Mid", "mean")
    )
    .reset_index()
)

salary_by_title = salary_by_title[salary_by_title["Job_Count"] >= 2]

salary_by_title = (
    salary_by_title
    .sort_values("Average_Salary", ascending=False)
    .head(10)
    .sort_values("Average_Salary")
)

salary_by_title["Average_Salary"] = salary_by_title["Average_Salary"].round()

salary_by_title = salary_by_title.rename(
    columns={
        "Job_Title": "Job Title",
        "Job_Count": "Number of Postings",
        "Average_Salary": "Average Estimated Salary"
    }
)

with st.container():
    render_html('<div class="content-card">')

    render_html(
        '<div class="subsection-title">'
        'Average Estimated Salary by Job Title'
        '</div>'
    )

    if len(salary_by_title) > 0:
        st.bar_chart(
            salary_by_title,
            x="Job Title",
            y="Average Estimated Salary",
            horizontal=True,
            color=ACCENT
        )
    else:
        st.info(
            "Not enough postings are available "
            "for salary comparison under the current filters."
        )

    render_html(
        '<div class="caption-note">'
        'Only job titles represented by at least two postings are included.'
        '</div>'
    )

    render_html("</div>")


# SALARY BY PROVINCE


salary_by_province = (
    filtered_jobs
    .dropna(subset=["Estimated_Annual_Mid"])
    .groupby("Province_Territory")
    .agg(
        Job_Count=("Province_Territory", "size"),
        Average_Salary=("Estimated_Annual_Mid", "mean")
    )
    .reset_index()
)

salary_by_province["Average_Salary"] = salary_by_province["Average_Salary"].round()

salary_by_province = salary_by_province.rename(
    columns={
        "Province_Territory": "Province / Territory",
        "Job_Count": "Number of Postings",
        "Average_Salary": "Average Estimated Salary"
    }
)

salary_by_province = salary_by_province.sort_values("Average Estimated Salary")

small_samples = salary_by_province[salary_by_province["Number of Postings"] < 3]

with st.container():
    render_html('<div class="content-card">')

    render_html(
        '<div class="subsection-title">'
        'Average Estimated Salary by Province / Territory'
        '</div>'
    )

    st.bar_chart(
        salary_by_province,
        x="Province / Territory",
        y="Average Estimated Salary",
        horizontal=True,
        color=CHART_COLOR
    )

    if len(small_samples) > 0:
        st.warning(
            "Some provincial salary averages are based on fewer than "
            "three postings and should be interpreted cautiously."
        )

    render_html("</div>")


# OCCUPATIONAL SKILLS


render_html('<div class="section-title">🧠 Occupational Skills & Competencies</div>')

render_html(
    """
    <div class="section-sub">
        OaSIS occupation-level skill ratings linked to the analyzed
        Job Bank occupations through NOC 2021 classifications.
    </div>
    """
)

skill_chart = skills.copy()
skill_chart["Average_Rating"] = skill_chart["Average_Rating"].round(2)
skill_chart = skill_chart.rename(columns={"Average_Rating": "Average Rating"})
skill_chart = skill_chart.sort_values("Average Rating")

with st.container():
    render_html('<div class="content-card">')

    st.bar_chart(
        skill_chart,
        x="Skill",
        y="Average Rating",
        horizontal=True,
        color="#2E5B9E"
    )

    render_html(
        '<div class="caption-note">'
        'Ratings use a 0–5 OaSIS scale. These are occupational '
        'competencies, not technology-frequency counts.'
        '</div>'
    )

    render_html("</div>")


# TECHNOLOGY DEMAND


render_html('<div class="section-title">💻 Technology Demand</div>')

render_html(
    """
    <div class="section-sub">
        Technology requirements recovered from verified direct
        Job Bank postings.
    </div>
    """
)

tech_sample = verified_technology_jobs[
    verified_technology_jobs["Province"].isin(selected_provinces)
    &
    verified_technology_jobs["Month"].isin(selected_months)
    &
    verified_technology_jobs["Job_Title"].isin(selected_titles)
].copy()

filtered_tech_mentions = technology_mentions[
    technology_mentions["Province"].isin(selected_provinces)
    &
    technology_mentions["Month"].isin(selected_months)
    &
    technology_mentions["Job_Title"].isin(selected_titles)
].copy()

technology_sample_size = tech_sample["WIC_ID"].nunique()
technology_with_requirements = filtered_tech_mentions["WIC_ID"].nunique()

with st.container():
    render_html('<div class="content-card">')

    if technology_sample_size > 0:

        filtered_demand = (
            filtered_tech_mentions
            .groupby("Technology")["WIC_ID"]
            .nunique()
            .reset_index(name="Postings Mentioning")
        )

        filtered_demand["Demand Percentage"] = (
            filtered_demand["Postings Mentioning"] / technology_sample_size * 100
        ).round(2)

        filtered_demand = (
            filtered_demand
            .sort_values(["Postings Mentioning", "Technology"], ascending=[False, True])
            .reset_index(drop=True)
        )

        top_technology = (
            filtered_demand.iloc[0]["Technology"] if len(filtered_demand) > 0 else "N/A"
        )

        tech_cols = st.columns(3)
        tech_cols[0].metric("Verified Sample", technology_sample_size)
        tech_cols[1].metric("Postings With Technology Data", technology_with_requirements)
        tech_cols[2].metric("Top Reported Technology", top_technology)

        render_html(
            """
            <div class="caption-note" style="margin-top:0.6rem;">
                Technology percentages use the verified direct Job Bank
                sample as the denominator.
            </div>
            """
        )

        generic_terms = [
            "Data Analysis Software",
            "Programming Software",
            "Database Software",
            "Spreadsheet Software",
            "Mapping and data visualization software",
            "Programming Languages",
            "Software Development",
            "Networking Software",
            "Network Security",
            "Internet",
            "Intranet"
        ]

        specific_technologies = filtered_demand[
            ~filtered_demand["Technology"].isin(generic_terms)
        ].copy()

        specific_technologies = (
            specific_technologies.head(15).sort_values("Postings Mentioning")
        )

        render_html("<hr>")

        render_html(
            '<div class="subsection-title">Specific Technologies &amp; Platforms</div>'
        )

        if len(specific_technologies) > 0:

            st.bar_chart(
                specific_technologies,
                x="Technology",
                y="Demand Percentage",
                horizontal=True,
                color=ACCENT
            )

            display_specific = (
                specific_technologies[
                    ["Technology", "Postings Mentioning", "Demand Percentage"]
                ]
                .sort_values("Postings Mentioning", ascending=False)
            )

            display_specific = display_specific.rename(
                columns={"Demand Percentage": "Demand (%)"}
            )

            st.dataframe(
                display_specific,
                hide_index=True,
                width="stretch",
                column_config={
                    "Demand (%)": st.column_config.NumberColumn(
                        "Demand (%)", format="%.2f%%"
                    )
                }
            )

        with st.expander("View all reported technology terms"):
            all_terms = filtered_demand.copy()

            st.dataframe(
                all_terms,
                hide_index=True,
                width="stretch",
                column_config={
                    "Demand Percentage": st.column_config.NumberColumn(
                        "Demand Percentage", format="%.2f%%"
                    )
                }
            )

    else:
        st.info(
            "No verified direct Job Bank technology records match "
            "the selected filters."
        )

    render_html("</div>")

st.warning(
    """
    Technology demand is based on a smaller verified sample of direct
    Job Bank postings because the monthly Job Bank open-data files do
    not contain full technology-requirement text.

    These percentages should therefore not be interpreted as
    representing all job postings in the main dataset.
    """
)

render_html("<hr>")



# EXPLORE JOB POSTINGS

render_html('<div class="section-title">📋 Explore Job Postings</div>')

display_jobs = filtered_jobs[
    [
        "Job_Title",
        "Province_Territory",
        "City",
        "Month",
        "Vacancy_Count",
        "Estimated_Annual_Mid"
    ]
].copy()

display_jobs = display_jobs.rename(
    columns={
        "Job_Title": "Job Title",
        "Province_Territory": "Province / Territory",
        "Vacancy_Count": "Vacancies",
        "Estimated_Annual_Mid": "Estimated Annual Salary"
    }
)

with st.container():
    render_html('<div class="content-card">')

    st.dataframe(
        display_jobs,
        width="stretch",
        hide_index=True,
        column_config={
            "Job Title": st.column_config.TextColumn("Job Title", width="large"),
            "Province / Territory": st.column_config.TextColumn(
                "Province / Territory", width="medium"
            ),
            "Estimated Annual Salary": st.column_config.NumberColumn(
                "Estimated Annual Salary", format="$%.0f"
            )
        }
    )

    render_html("</div>")


# METHODOLOGY


with st.expander("ℹ️ About the Data & Methodology"):

    st.markdown(
        """
### Job Market Data

Government of Canada **Job Bank monthly open-data files**
from **March through July 2026** were used to measure:

- job-posting volume
- geographic demand
- job-title distribution
- salary patterns
- vacancy counts


### Salary Standardization

Hourly salaries were converted using:

**40 hours/week × 52 weeks/year**

Bi-weekly salaries were converted using:

**26 pay periods/year**

Clearly malformed salary records were excluded from
salary analysis while their job postings were retained
where appropriate for other analyses.


### Occupational Skills

Government of Canada **OaSIS** occupational profiles
were linked to Job Bank postings using **NOC 2021 codes**.

These ratings represent occupational competencies such as:

- Problem Solving
- Digital Literacy
- Critical Thinking
- Systems Analysis
- Numeracy


### Technology Demand

The monthly Job Bank CSV files do not contain full
job-requirement text.

A subset of **direct Job Bank postings** was therefore
matched to archived Job Bank information.

Technology demand is calculated only from postings for
which technology information could be reliably verified.

Technology requirements and OaSIS occupational
competencies are intentionally analyzed separately.
        """
    )


# FOOTER

render_html(
    '<div class="caption-note" style="text-align:center; margin-top:1.4rem;">'
    'Canadian Data Job Market Analysis &nbsp;|&nbsp; '
    'Government of Canada Job Bank + OaSIS'
    '</div>'
)