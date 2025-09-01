# Evals Suite 

Sutie for running sandbagging evaluations for MATS project

To set up: 
1. Clone the repo
2. Install dependencies with uv. Can do a uv sync --dev, or just run the framework with "uv run src/run_evals.py" & it should do it automatically.
3. Set up your .vscode/settings.json as specified below
4. Copy your .env file with api keys to the root of the repo
5. Ensure vscode discovers the right python environment in .venv. This will also enable the inspect-ai extension to work.
6. See if the inspect-ai extension logviewer is the default way to open the logfile. If not, change the default program to open .json files with to the inspect-ai logviewer under the "Open With" right-click option in vscode.








##.vscode/settings.json
{
    "workbench.editorAssociations": {
        "*.ipynb": "jupyter-notebook",
        "{[0-9][0-9][0-9][0-9]}-{[0-9][0-9]}-{[0-9][0-9]}T{[0-9][0-9]}[:-]{[0-9][0-9]}[:-]{[0-9][0-9]}*{[A-Za-z0-9]{21}}*.json": "inspect-ai.log-editor"
    },

    "files.exclude": {
        "**/node_modules/**": true,
        "**/.mypy_cache/**": true,
        "**/__pycache__/**": true,
        "**/.pytest_cache/**": true,
        "**/__init__.py": true,
    }
}