# Deployment checklist — Streamlit Community Cloud

## Before deployment
- [ ] Push the full project directory to a GitHub repository.
- [ ] Ensure `app.py`, `requirements.txt`, and `packages.txt` are at the repository root.
- [ ] Confirm `packages.txt` contains `g++`.
- [ ] Confirm the C++ source files are committed; do not commit `.build/` binaries.
- [ ] Keep sample CSV files in `data/`.

## Deploy
1. Sign in to Streamlit Community Cloud with the GitHub account that owns the repository.
2. Create a new app and select the repository, branch and `app.py` entry point.
3. Deploy and wait for dependency installation and app startup.
4. Open the generated URL and test Overview, Discover, My Profile, Exchanges and Analytics.
5. Send an exchange request from S001 to S002, switch the demo identity to S002, and accept it.
6. Record the final URL and add it to the report and README.

The cloud environment must permit installing g++ and compiling the C++ engine. If the provider changes its build image or package policy, deployment configuration may need adjustment. The app's C++ build errors are shown in the Streamlit page for diagnosis.

## Important
A public URL cannot be created from the source ZIP alone. Deployment must be performed from the team's own GitHub/Streamlit account. Do not put private credentials in the repository.
