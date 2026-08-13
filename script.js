// DATA


let jobs = [];
let skills = [];
let technologyMentions = [];
let verifiedTechnologyJobs = [];

let filteredJobs = [];

let tableLimit = 20;


// CHART REFERENCES

let provinceChart;
let monthlyChart;
let titlesChart;
let salaryTitleChart;
let salaryProvinceChart;
let skillsChart;
let technologyChart;



// COLORS
const PRIMARY = "#1B3B6F";
const ACCENT = "#D62828";


// LOADER


function loadCSV(path) {

    return new Promise(
        (resolve, reject) => {

            Papa.parse(
                path,
                {
                    download: true,
                    header: true,
                    skipEmptyLines: true,

                    complete: results => {
                        resolve(results.data);
                    },

                    error: error => {
                        reject(error);
                    }
                }
            );

        }
    );

}


// START 


document.addEventListener(
    "DOMContentLoaded",
    async () => {

        try {

            jobs = await loadCSV(
                "data/processed/canada_data_jobs_clean.csv"
            );

            skills = await loadCSV(
                "data/processed/skill_summary.csv"
            );

            technologyMentions = await loadCSV(
                "data/processed/technology_mentions.csv"
            );

            verifiedTechnologyJobs = await loadCSV(
                "data/processed/verified_technology_jobs.csv"
            );


            cleanData();

            setupFilters();

            setupEvents();

            updateDashboard();


        } catch (error) {

            console.error(
                "Error loading dashboard data:",
                error
            );

            alert(
                "The dashboard data could not be loaded. " +
                "If you opened index.html directly from your computer, " +
                "use Live Server or open the deployed GitHub Pages version."
            );

        }

    }
);


// DATA


function cleanData() {

    jobs = jobs.map(
        row => ({

            ...row,

            Vacancy_Count:
                parseFloat(
                    row.Vacancy_Count
                ) || 0,

            Estimated_Annual_Mid:
                parseFloat(
                    row.Estimated_Annual_Mid
                )

        })
    );


    skills = skills.map(
        row => ({

            ...row,

            Average_Rating:
                parseFloat(
                    row.Average_Rating
                ) || 0

        })
    );


    technologyMentions =
        technologyMentions.map(
            row => ({

                ...row,

                Month:
                    String(
                        row.Posting_Date
                    ).slice(
                        0,
                        7
                    )

            })
        );


    verifiedTechnologyJobs =
        verifiedTechnologyJobs.map(
            row => ({

                ...row,

                Month:
                    String(
                        row.Posting_Date
                    ).slice(
                        0,
                        7
                    )

            })
        );

}


// FILTER SETUP


function setupFilters() {

    const provinceFilter =
        document.getElementById(
            "provinceFilter"
        );

    const monthFilter =
        document.getElementById(
            "monthFilter"
        );

    const jobTitleFilter =
        document.getElementById(
            "jobTitleFilter"
        );


    const provinces = [
        ...new Set(
            jobs
            .map(
                row =>
                    row.Province_Territory
            )
            .filter(Boolean)
        )
    ].sort();


    provinces.forEach(
        province => {

            provinceFilter.add(
                new Option(
                    province,
                    province
                )
            );

        }
    );


    const months = [
        ...new Set(
            jobs
            .map(
                row =>
                    row.Month
            )
            .filter(Boolean)
        )
    ].sort();


    months.forEach(
        month => {

            monthFilter.add(
                new Option(
                    month,
                    month
                )
            );

        }
    );


    const titles = [
        ...new Set(
            jobs
            .map(
                row =>
                    row.Job_Title
            )
            .filter(Boolean)
        )
    ].sort();


    titles.forEach(
        title => {

            jobTitleFilter.add(
                new Option(
                    title,
                    title
                )
            );

        }
    );

}


// EVENTS


function setupEvents() {

    document
    .getElementById(
        "provinceFilter"
    )
    .addEventListener(
        "change",
        updateDashboard
    );


    document
    .getElementById(
        "monthFilter"
    )
    .addEventListener(
        "change",
        updateDashboard
    );


    document
    .getElementById(
        "jobTitleFilter"
    )
    .addEventListener(
        "change",
        updateDashboard
    );


    document
    .getElementById(
        "resetFilters"
    )
    .addEventListener(
        "click",
        () => {

            document.getElementById(
                "provinceFilter"
            ).value = "All";

            document.getElementById(
                "monthFilter"
            ).value = "All";

            document.getElementById(
                "jobTitleFilter"
            ).value = "All";

            tableLimit = 20;

            updateDashboard();

        }
    );


    document
    .getElementById(
        "showMoreJobs"
    )
    .addEventListener(
        "click",
        () => {

            tableLimit += 20;

            updateTable();

        }
    );

}


// CURRENT FILTER 


function getFilters() {

    return {

        province:
            document.getElementById(
                "provinceFilter"
            ).value,

        month:
            document.getElementById(
                "monthFilter"
            ).value,

        title:
            document.getElementById(
                "jobTitleFilter"
            ).value

    };

}



// JOB FILTERS


function applyFilters() {

    const filters =
        getFilters();


    filteredJobs =
        jobs.filter(
            row => {

                const provinceMatch =
                    filters.province === "All"
                    ||
                    row.Province_Territory
                    === filters.province;


                const monthMatch =
                    filters.month === "All"
                    ||
                    row.Month
                    === filters.month;


                const titleMatch =
                    filters.title === "All"
                    ||
                    row.Job_Title
                    === filters.title;


                return (
                    provinceMatch
                    &&
                    monthMatch
                    &&
                    titleMatch
                );

            }
        );

}


// UPDATE 


function updateDashboard() {

    tableLimit = 20;

    applyFilters();

    updateKPIs();

    updateProvinceChart();

    updateMonthlyChart();

    updateTitlesChart();

    updateSalaryTitleChart();

    updateSalaryProvinceChart();

    updateSkillsChart();

    updateTechnology();

    updateTable();

}



// KPI


function updateKPIs() {

    const totalJobs =
        filteredJobs.length;


    const totalVacancies =
        filteredJobs.reduce(
            (sum, row) =>
                sum
                +
                row.Vacancy_Count,
            0
        );


    const provinceCount =
        new Set(
            filteredJobs.map(
                row =>
                    row.Province_Territory
            )
        ).size;


    const salaryValues =
        filteredJobs
        .map(
            row =>
                row.Estimated_Annual_Mid
        )
        .filter(
            value =>
                Number.isFinite(
                    value
                )
        );


    const averageSalary =
        salaryValues.length
        ?
        salaryValues.reduce(
            (a, b) =>
                a + b,
            0
        )
        /
        salaryValues.length
        :
        null;


    document.getElementById(
        "totalJobs"
    ).textContent =
        totalJobs.toLocaleString();


    document.getElementById(
        "totalVacancies"
    ).textContent =
        Math.round(
            totalVacancies
        ).toLocaleString();


    document.getElementById(
        "provinceCount"
    ).textContent =
        provinceCount;


    document.getElementById(
        "averageSalary"
    ).textContent =
        averageSalary
        ?
        "$"
        +
        Math.round(
            averageSalary
        ).toLocaleString()
        :
        "N/A";

}


// COUNTER UTILITY


function countBy(
    data,
    key
) {

    const counts = {};


    data.forEach(
        row => {

            const value =
                row[key];

            if (!value) {
                return;
            }

            counts[value] =
                (
                    counts[value]
                    ||
                    0
                )
                +
                1;

        }
    );


    return counts;

}

// DESTROY CHART


function destroyChart(
    chart
) {

    if (chart) {
        chart.destroy();
    }

}


// PROVINCE CHART


function updateProvinceChart() {

    const counts =
        countBy(
            filteredJobs,
            "Province_Territory"
        );


    const entries =
        Object.entries(
            counts
        )
        .sort(
            (a, b) =>
                a[1] - b[1]
        );


    destroyChart(
        provinceChart
    );


    provinceChart =
        new Chart(
            document.getElementById(
                "provinceChart"
            ),
            {

                type: "bar",

                data: {

                    labels:
                        entries.map(
                            item =>
                                item[0]
                        ),

                    datasets: [
                        {

                            label:
                                "Job Postings",

                            data:
                                entries.map(
                                    item =>
                                        item[1]
                                ),

                            backgroundColor:
                                PRIMARY

                        }
                    ]

                },

                options: {

                    indexAxis: "y",

                    responsive: true,

                    plugins: {

                        legend: {
                            display: false
                        }

                    }

                }

            }
        );

}


// MONTH CHART


function updateMonthlyChart() {

    const counts =
        countBy(
            filteredJobs,
            "Month"
        );


    const entries =
        Object.entries(
            counts
        )
        .sort(
            (a, b) =>
                a[0]
                .localeCompare(
                    b[0]
                )
        );


    destroyChart(
        monthlyChart
    );


    monthlyChart =
        new Chart(
            document.getElementById(
                "monthlyChart"
            ),
            {

                type: "line",

                data: {

                    labels:
                        entries.map(
                            item =>
                                item[0]
                        ),

                    datasets: [
                        {

                            label:
                                "Job Postings",

                            data:
                                entries.map(
                                    item =>
                                        item[1]
                                ),

                            borderColor:
                                PRIMARY,

                            backgroundColor:
                                PRIMARY,

                            tension: 0.25

                        }
                    ]

                },

                options: {

                    responsive: true,

                    plugins: {

                        legend: {
                            display: false
                        }

                    }

                }

            }
        );

}


// TITLE CHART


function updateTitlesChart() {

    const counts =
        countBy(
            filteredJobs,
            "Job_Title"
        );


    const entries =
        Object.entries(
            counts
        )
        .sort(
            (a, b) =>
                b[1] - a[1]
        )
        .slice(
            0,
            10
        )
        .sort(
            (a, b) =>
                a[1] - b[1]
        );


    destroyChart(
        titlesChart
    );


    titlesChart =
        new Chart(
            document.getElementById(
                "titlesChart"
            ),
            {

                type: "bar",

                data: {

                    labels:
                        entries.map(
                            item =>
                                item[0]
                        ),

                    datasets: [
                        {

                            data:
                                entries.map(
                                    item =>
                                        item[1]
                                ),

                            backgroundColor:
                                PRIMARY

                        }
                    ]

                },

                options: {

                    indexAxis: "y",

                    plugins: {

                        legend: {
                            display: false
                        }

                    }

                }

            }
        );

}

// GROUP SALARY 


function averageSalaryBy(
    data,
    key
) {

    const groups = {};


    data.forEach(
        row => {

            const category =
                row[key];

            const salary =
                row.Estimated_Annual_Mid;


            if (
                !category
                ||
                !Number.isFinite(
                    salary
                )
            ) {
                return;
            }


            if (
                !groups[
                    category
                ]
            ) {

                groups[
                    category
                ] = [];

            }


            groups[
                category
            ].push(
                salary
            );

        }
    );


    return Object.entries(
        groups
    ).map(
        ([category, salaries]) => {

            const average =
                salaries.reduce(
                    (a, b) =>
                        a + b,
                    0
                )
                /
                salaries.length;


            return {

                category,

                average,

                count:
                    salaries.length

            };

        }
    );

}


// SALARY TITLE


function updateSalaryTitleChart() {

    const entries =
        averageSalaryBy(
            filteredJobs,
            "Job_Title"
        )
        .filter(
            item =>
                item.count >= 2
        )
        .sort(
            (a, b) =>
                b.average
                -
                a.average
        )
        .slice(
            0,
            10
        )
        .sort(
            (a, b) =>
                a.average
                -
                b.average
        );


    destroyChart(
        salaryTitleChart
    );


    salaryTitleChart =
        new Chart(
            document.getElementById(
                "salaryTitleChart"
            ),
            {

                type: "bar",

                data: {

                    labels:
                        entries.map(
                            item =>
                                item.category
                        ),

                    datasets: [
                        {

                            data:
                                entries.map(
                                    item =>
                                        Math.round(
                                            item.average
                                        )
                                ),

                            backgroundColor:
                                ACCENT

                        }
                    ]

                },

                options: {

                    indexAxis: "y",

                    plugins: {

                        legend: {
                            display: false
                        }

                    }

                }

            }
        );

}


// SALARY PROVINCE


function updateSalaryProvinceChart() {

    const entries =
        averageSalaryBy(
            filteredJobs,
            "Province_Territory"
        )
        .sort(
            (a, b) =>
                a.average
                -
                b.average
        );


    const hasSmallSamples =
        entries.some(
            item =>
                item.count < 3
        );


    document.getElementById(
        "salaryWarning"
    ).classList.toggle(
        "hidden",
        !hasSmallSamples
    );


    destroyChart(
        salaryProvinceChart
    );


    salaryProvinceChart =
        new Chart(
            document.getElementById(
                "salaryProvinceChart"
            ),
            {

                type: "bar",

                data: {

                    labels:
                        entries.map(
                            item =>
                                item.category
                        ),

                    datasets: [
                        {

                            data:
                                entries.map(
                                    item =>
                                        Math.round(
                                            item.average
                                        )
                                ),

                            backgroundColor:
                                PRIMARY

                        }
                    ]

                },

                options: {

                    indexAxis: "y",

                    plugins: {

                        legend: {
                            display: false
                        }

                    }

                }

            }
        );

}


// SKILLS


function updateSkillsChart() {

    const entries =
        [...skills]
        .sort(
            (a, b) =>
                a.Average_Rating
                -
                b.Average_Rating
        );


    destroyChart(
        skillsChart
    );


    skillsChart =
        new Chart(
            document.getElementById(
                "skillsChart"
            ),
            {

                type: "bar",

                data: {

                    labels:
                        entries.map(
                            row =>
                                row.Skill
                        ),

                    datasets: [
                        {

                            data:
                                entries.map(
                                    row =>
                                        row.Average_Rating
                                ),

                            backgroundColor:
                                "#2E5B9E"

                        }
                    ]

                },

                options: {

                    indexAxis: "y",

                    plugins: {

                        legend: {
                            display: false
                        }

                    },

                    scales: {

                        x: {

                            min: 0,

                            max: 5

                        }

                    }

                }

            }
        );

}


// FILTER

function techRowMatches(
    row,
    filters
) {

    const provinceMatch =
        filters.province
        === "All"
        ||
        row.Province
        === filters.province;


    const monthMatch =
        filters.month
        === "All"
        ||
        row.Month
        === filters.month;


    const titleMatch =
        filters.title
        === "All"
        ||
        row.Job_Title
        === filters.title;


    return (
        provinceMatch
        &&
        monthMatch
        &&
        titleMatch
    );

}


// UPDATE


function updateTechnology() {

    const filters =
        getFilters();


    const sample =
        verifiedTechnologyJobs
        .filter(
            row =>
                techRowMatches(
                    row,
                    filters
                )
        );


    const mentions =
        technologyMentions
        .filter(
            row =>
                techRowMatches(
                    row,
                    filters
                )
        );


    const sampleIds =
        new Set(
            sample.map(
                row =>
                    row.WIC_ID
            )
        );


    const techPostingIds =
        new Set(
            mentions.map(
                row =>
                    row.WIC_ID
            )
        );


    const sampleSize =
        sampleIds.size;


    const technologyCounts = {};


    mentions.forEach(
        row => {

            if (
                !technologyCounts[
                    row.Technology
                ]
            ) {

                technologyCounts[
                    row.Technology
                ] =
                    new Set();

            }


            technologyCounts[
                row.Technology
            ].add(
                row.WIC_ID
            );

        }
    );


    const genericTerms =
        new Set(
            [
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
        );


    const entries =
        Object.entries(
            technologyCounts
        )
        .map(
            ([technology, ids]) => ({

                technology,

                count:
                    ids.size,

                percentage:
                    sampleSize
                    ?
                    (
                        ids.size
                        /
                        sampleSize
                        *
                        100
                    )
                    :
                    0

            })
        )
        .sort(
            (a, b) =>
                b.count - a.count
                ||
                a.technology.localeCompare(
                    b.technology
                )
        );


    const specific =
        entries
        .filter(
            item =>
                !genericTerms.has(
                    item.technology
                )
        )
        .slice(
            0,
            15
        )
        .reverse();


    document.getElementById(
        "verifiedSample"
    ).textContent =
        sampleSize;


    document.getElementById(
        "techPostings"
    ).textContent =
        techPostingIds.size;


    document.getElementById(
        "topTechnology"
    ).textContent =
        entries.length
        ?
        entries[0].technology
        :
        "N/A";


    destroyChart(
        technologyChart
    );


    technologyChart =
        new Chart(
            document.getElementById(
                "technologyChart"
            ),
            {

                type: "bar",

                data: {

                    labels:
                        specific.map(
                            item =>
                                item.technology
                        ),

                    datasets: [
                        {

                            data:
                                specific.map(
                                    item =>
                                        Number(
                                            item.percentage.toFixed(
                                                2
                                            )
                                        )
                                ),

                            backgroundColor:
                                ACCENT

                        }
                    ]

                },

                options: {

                    indexAxis: "y",

                    plugins: {

                        legend: {
                            display: false
                        },

                        tooltip: {

                            callbacks: {

                                label:
                                    context =>
                                        context.raw
                                        +
                                        "%"

                            }

                        }

                    },

                    scales: {

                        x: {

                            title: {

                                display: true,

                                text:
                                    "Demand Percentage (%)"

                            }

                        }

                    }

                }

            }
        );

}


// JOB TABLE


function updateTable() {

    const tbody =
        document.getElementById(
            "jobsTableBody"
        );


    tbody.innerHTML = "";


    const rows =
        filteredJobs.slice(
            0,
            tableLimit
        );


    rows.forEach(
        row => {

            const tr =
                document.createElement(
                    "tr"
                );


            const salary =
                Number.isFinite(
                    row.Estimated_Annual_Mid
                )
                ?
                "$"
                +
                Math.round(
                    row.Estimated_Annual_Mid
                ).toLocaleString()
                :
                "N/A";


            tr.innerHTML = `

                <td>
                    ${escapeHTML(
                        row.Job_Title
                        ||
                        ""
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        row.Province_Territory
                        ||
                        ""
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        row.City
                        ||
                        ""
                    )}
                </td>

                <td>
                    ${escapeHTML(
                        row.Month
                        ||
                        ""
                    )}
                </td>

                <td>
                    ${Math.round(
                        row.Vacancy_Count
                    )}
                </td>

                <td>
                    ${salary}
                </td>

            `;


            tbody.appendChild(
                tr
            );

        }
    );


    const button =
        document.getElementById(
            "showMoreJobs"
        );


    button.style.display =
        tableLimit
        <
        filteredJobs.length
        ?
        "inline-block"
        :
        "none";

}


// HTML
function escapeHTML(
    value
) {

    return String(
        value
    )
    .replace(
        /&/g,
        "&amp;"
    )
    .replace(
        /</g,
        "&lt;"
    )
    .replace(
        />/g,
        "&gt;"
    )
    .replace(
        /"/g,
        "&quot;"
    )
    .replace(
        /'/g,
        "&#039;"
    );

}