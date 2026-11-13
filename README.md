# SkillLoop – Campus Skill Exchange

SkillLoop is a platform where students can teach each other skills and learn new things from their classmates.

For example, a student who knows Python can teach another student who wants to learn Python. The platform helps students find suitable learning partners based on their skills, availability and learning preferences.

The project uses C++ for its main working logic, Python for the interface and data analysis, and Streamlit to display the application.

## Features

- Students can view and manage their profiles.
- Students can add skills they can teach.
- Students can add skills they want to learn.
- The platform finds students with matching skills.
- Students can send, accept or decline exchange requests.
- The application shows basic charts and analysis of student skills.

## Technologies Used

- **C++17:** Used for classes, student records and matching logic.
- **Python:** Used to connect the C++ engine with the application and perform data analysis.
- **Streamlit:** Used to create the application interface.
- **Pandas:** Used to read and analyse student data.
- **Matplotlib:** Used to create graphs.
- **CSV:** Used to store student and exchange information.
- **g++:** Used to compile the C++ code.

## How to Run the Project

### 1. Install the required software

You need:
- Python 3.10 or above
- g++ compiler

### 2. Open the project folder

Extract the project folder and open a terminal inside it.

### 3. Create a virtual environment (recommended)

**For Windows PowerShell:**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**For macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install the required packages

```bash
python -m pip install -r requirements.txt
```

### 5. Start the application

```bash
streamlit run app.py
```

After running the command, open the local link shown in your terminal. It is normally:

`http://localhost:8501`

The Python program automatically compiles the C++ code when the application runs for the first time.

## Windows Compiler Help

The project automatically builds the C++ program when needed.

If you face a compilation error:

1. Check whether g++ is installed.
2. Open PowerShell and run:

```powershell
g++ --version
```

3. Run the tests to check whether the C++ engine is working:

```powershell
python -m unittest discover -s tests -v
```

If you have more than one g++ installation, you can select one using:

```powershell
$env:CXX = (Get-Command g++).Source
python -m streamlit run app.py
```

## Deploying the Project

You can also host SkillLoop using Streamlit Community Cloud.

1. Upload the complete project to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app and connect your GitHub repository.
4. Select `app.py` as the main file.
5. Make sure `requirements.txt` and `packages.txt` are present in the main project folder.
6. Deploy the application.

The `packages.txt` file is used to install g++ on the cloud system.

The application builds the C++ engine when it starts for the first time. Hosting depends on the platform's available resources and build settings.

## Sample Student Accounts

The project includes four sample student profiles:

| Student ID | Name | Course | Year |
|---|---|---|---|
| S001 | Aman | Computer Science | 2 |
| S002 | Iksha | Computer Science | 2 |
| S003 | Riya | Information Technology | 3 |
| S004 | Kabir | Computer Science | 1 |

You can switch between these profiles using the profile selector in the sidebar.

The Discover page shows students who have matching skills. You can also try sending exchange requests and accepting or declining them by switching to the other student's profile.

## Project Folder Structure

```text
SkillLoop/
│
├── app.py                  # Main Streamlit application
├── engine.py               # Connects Python with C++
├── requirements.txt        # Python packages
├── packages.txt            # Packages needed for deployment
│
├── cpp_engine/
│   └── src/main.cpp        # Main C++ code and classes
│
├── data/
│   ├── students.csv        # Student information
│   └── exchanges.csv       # Exchange request information
│
├── analytics/
│   └── analyse.py          # Data analysis code
│
├── tests/                  # Project tests
│
└── docs/                   # Project documentation
```

## Running the Tests

To check whether the project is working correctly, run:

```bash
python -m unittest discover -s tests -v
```

This runs the available tests for the C++ engine and its features.

## C++ Engine Commands

The C++ program can also be run directly from the terminal.

First, compile the program:

```bash
g++ -std=c++17 -O2 cpp_engine/src/main.cpp -o skillloop_engine
```

Then you can use these commands:

```bash
./skillloop_engine init data
./skillloop_engine students data
./skillloop_engine matches data S001
./skillloop_engine create_exchange data S001 S002 Python
./skillloop_engine exchanges data
```

On Windows, use `skillloop_engine.exe` instead of `skillloop_engine`.

## How the Matching System Works

SkillLoop uses a rule-based matching system.

It checks whether two students can help each other learn the skills they want. It also considers their availability and preferred learning method to calculate a match score.

The project does not use Machine Learning or Artificial Intelligence. The matching and score calculation are handled by the C++ program.

## Data Analysis

The Python analytics module uses Pandas and Matplotlib to study the skills listed by students.

It helps us understand:
- Which skills students can teach.
- Which skills students want to learn.
- The difference between available skills and demanded skills.

The results are saved as CSV files and graphs.

## Limitations

- The project does not have a complete login or authentication system.
- The profile selector is used only to switch between sample student accounts.
- CSV files are used for storing data, so the project is designed for a small demonstration.
- The matching system uses simple rules instead of machine learning.
- The project is not designed for many users making changes at the same time.

## Future Improvements

Some features that can be added in the future are:

- A proper student login and registration system.
- A database instead of CSV files.
- Notifications for new exchange requests.
- More advanced student matching.
- Ratings and feedback after completing a skill exchange.

## Team Members

**Iksha**
- Python-based data analysis using Pandas and Matplotlib.
- C++ abstraction and inheritance.

**Aman Gemawat**
- Streamlit frontend development.
- C++ encapsulation and polymorphism.

For detailed individual contributions, please refer to the project report.
