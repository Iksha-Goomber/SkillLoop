# SkillLoop Architecture

## Layered design

1. **Presentation — `app.py` (Streamlit):** renders pages, collects input, and presents C++ results. It does not implement matching rules.
2. **Adapter — `engine.py`:** compiles the C++ source when necessary and invokes the engine through a safe argument-list subprocess call. Tab-separated output is converted into Python rows.
3. **Domain and application — `cpp_engine/`:** owns `User`, `Student`, `Admin`, `Match`, student search, matching, exchanges and CSV persistence.
4. **Storage — `data/*.csv`:** portable demonstration storage.
5. **Analytics — `analytics/analyse.py`:** uses pandas to summarise supply and demand from CSV exports.

## Class relationships

- `User` is an abstract base class. It contains private identity fields and pure virtual `role()` and `dashboardMessage()` methods.
- `Student` and `Admin` publicly inherit from `User` and override the virtual methods.
- `Match` encapsulates a match candidate and score; `operator>` compares scores and is used by the sorting algorithm.
- `DataManager` reads and writes student and exchange records.
- `StudentService` provides three overloaded `searchStudents` signatures: by name, by name + course, and by name + year.
- `MatchEngine` calculates reciprocal compatibility and returns ranked `Match` objects.
- `ExchangeService` creates exchange requests through `DataManager`.

## Runtime flow

A user selects a demo student in Streamlit. The Discover page calls `engine.matches(student_id)`. The adapter launches the C++ executable. C++ loads the CSV records, constructs `Student` objects, runs `MatchEngine::findMatches`, sorts `Match` objects using the overloaded comparison operator, and prints tab-separated result rows. Streamlit renders those rows as cards.

## Why subprocess rather than Qt or a Python-only implementation?

The application must be easy to host and open in a browser while the assessed business logic remains C++. A small command-line boundary keeps the C++ engine independently compilable and testable. Streamlit communicates with it without requiring Qt, Node, or a JavaScript frontend. The same engine can be demonstrated directly from a terminal.


The C++ implementation is kept in `cpp_engine/src/main.cpp` so the class declarations and function definitions can be studied together in one file. The Python adapter compiles this single source file.
