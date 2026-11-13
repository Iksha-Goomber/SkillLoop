# SkillLoop — Campus Skill Exchange

A student-to-student skill exchange platform built as an academic C++ OOP project. The **C++17 engine owns the domain model, matching rules, student records, and exchange workflow**. Streamlit is the browser-based presentation layer; Python analytics reads the same CSV data.

## Technology
- C++17: OOP domain model and business logic
- Streamlit: browser UI
- Python: UI adapter and analytics
- CSV: lightweight persistent storage
- g++: compile the C++ engine at first launch

## Run locally (Windows / macOS / Linux)

1. Install Python 3.10+ and a C++17 compiler (`g++`).
2. Extract this folder and open a terminal in the project root.
3. Create and activate a virtual environment (recommended):

   **Windows PowerShell**
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install Python packages and launch:
   ```bash
   python -m pip install -r requirements.txt
   streamlit run app.py
   ```
5. Open the local URL printed by Streamlit (normally http://localhost:8501).

The Python adapter compiles the C++ sources into `.build/` automatically on first launch. No Qt installation or CMake setup is required.


## Windows compiler troubleshooting

The Python adapter builds the C++ engine automatically. On Windows it writes the executable as
`.build/skillloop_engine.exe` and invokes the compiler from the project directory using
project-relative source paths. This avoids common MSYS2/MinGW path-conversion problems when
Python launches `g++`.

If compilation fails, the app now displays the compiler name, exit code, command, and captured
diagnostic output. To verify the engine independently, run:

```powershell
python -m unittest discover -s tests -v
```

The test suite compiles a temporary `engine.exe` and prints the full compiler diagnostic if
that build fails. Make sure `g++ --version` works in the same terminal where you launch
Streamlit. If you have multiple compiler installations, you can select one explicitly in
PowerShell before launching:

```powershell
$env:CXX = (Get-Command g++).Source
python -m streamlit run app.py
```

## Deploy on Streamlit Community Cloud
1. Push the complete project folder to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository and select `app.py` as the entry point.
3. Keep `packages.txt` at the repository root; it asks the Linux build image to install `g++`.
4. Keep `requirements.txt` at the repository root.
5. Deploy. The app compiles the C++ engine on its first startup.

Cloud hosting is subject to the provider's current build-image policies and resource limits. Test the deployed URL after each deployment; a ZIP alone is not a hosted URL.

## Included sample accounts
- S001 — Aman (Computer Science, Year 2)
- S002 — Iksha (Computer Science, Year 2)
- S003 — Riya (Information Technology, Year 3)
- S004 — Kabir (Computer Science, Year 1)

Use the profile selector in the sidebar to switch demo identities. The Discover page demonstrates reciprocal matches. Requests can be accepted or declined by switching to the recipient profile.

## Project layout
```text
SkillLoop/
├── app.py                  # Streamlit interface
├── engine.py               # Python-to-C++ subprocess adapter
├── requirements.txt
├── packages.txt            # g++ for Streamlit Cloud
├── cpp_engine/             # C++ OOP engine
│   └── src/main.cpp         # Classes, functions and program entry point
├── data/                    # CSV persistence
├── analytics/               # Standalone analytics script
├── tests/                   # Automated C++ integration tests
└── docs/                    # Architecture, algorithms, viva and report
```

## Run tests
```bash
python -m unittest discover -s tests -v
```

## C++ engine commands
The engine is intentionally callable from the terminal for demonstration:
```bash
g++ -std=c++17 -O2 cpp_engine/src/main.cpp -o skillloop_engine
./skillloop_engine init data
./skillloop_engine students data
./skillloop_engine matches data S001
./skillloop_engine create_exchange data S001 S002 Python
./skillloop_engine exchanges data
```
On Windows, use `skillloop_engine.exe` as the output filename and run it from PowerShell.

## Academic note
The matching method is a transparent **rule-based algorithm**, not machine learning or AI. C++ performs the reciprocal matching and score calculation. Python is used for the web interface and descriptive analytics only. Do not describe the project as an AI recommender.

## Known scope limits
- Authentication is intentionally omitted; the sidebar profile selector is a classroom demo identity switcher, not secure login.
- CSV storage is suitable for a small demonstration, not concurrent production use.
- Student records are append/update CSV records; no password or sensitive account information is collected.
- Availability and learning mode influence the score using simple exact/partial matching rules.
