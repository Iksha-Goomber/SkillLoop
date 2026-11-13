"""Simple descriptive analysis for SkillLoop student skills."""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# Find the project folders.
PROJECT_FOLDER = Path(__file__).resolve().parents[1]
DATA_FOLDER = PROJECT_FOLDER / "data"
OUTPUT_FOLDER = Path(__file__).resolve().parent / "output"

OUTPUT_FOLDER.mkdir(exist_ok=True)

# Read student information from the CSV file.
students = pd.read_csv(DATA_FOLDER / "students.csv")

if students.empty:
    print("No student records found. Add students in the SkillLoop app first.")
    raise SystemExit

# Get the skills that students can teach.
offered_skills = students["teaches"].fillna("")
offered_skills = offered_skills.str.split(";").explode()
offered_skills = offered_skills.str.strip()
offered_skills = offered_skills[offered_skills != ""]

# Count how many students can teach each skill.
offered_count = offered_skills.value_counts()

# Get the skills that students want to learn.
wanted_skills = students["learns"].fillna("")
wanted_skills = wanted_skills.str.split(";").explode()
wanted_skills = wanted_skills.str.strip()
wanted_skills = wanted_skills[wanted_skills != ""]

# Count how many students want to learn each skill.
wanted_count = wanted_skills.value_counts()

# Put offered and wanted counts together in one table.
summary = pd.DataFrame({
    "Offered": offered_count,
    "Wanted": wanted_count
})

summary = summary.fillna(0).astype(int)
summary.index.name = "skill"
summary = summary.reset_index()

# A positive gap means more students want the skill than can teach it.
summary["Demand gap"] = summary["Wanted"] - summary["Offered"]

# Save the skill summary so it can be used elsewhere in the project.
summary.to_csv(OUTPUT_FOLDER / "skill_summary.csv", index=False)


def make_skill_chart(data, column_name, chart_title, file_name):
    """Create a horizontal bar chart for the ten most common skills."""

    top_skills = data.nlargest(10, column_name)
    top_skills = top_skills.sort_values(column_name)

    plt.figure(figsize=(8, 5))
    plt.barh(top_skills["skill"], top_skills[column_name])
    plt.title(chart_title)
    plt.xlabel("Number of students")
    plt.tight_layout()

    plt.savefig(OUTPUT_FOLDER / file_name, dpi=160)
    plt.close()


# Create one chart for skills offered and another for skills wanted.
make_skill_chart(
    summary,
    "Offered",
    "Most offered skills",
    "skills_offered.png"
)

make_skill_chart(
    summary,
    "Wanted",
    "Most wanted skills",
    "skills_wanted.png"
)

print("Analytics saved in:", OUTPUT_FOLDER)
