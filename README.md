# Evals Suite 

Sutie for running sandbagging evaluations for MATS project


## Setup Instructions
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

## Use Instructions

### Quick Start

1. **Set up API keys** - Create a `.env` file in the repository root:
   ```bash
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   ```

2. **Run an evaluation** - Use a config file to define your experiment:
   ```bash
   uv run src/run_evals.py --config config_files/your_config.yaml --name experiment_name
   ```

### Configuration Files

Experiments are defined via YAML config files that specify:
- Model to evaluate (e.g., GPT-4, Claude)
- Benchmark tasks to run
- Sandbagging parameters
- Output settings

Example config structure: See the reference config files in each task experiment directory.

### Running Experiments

```bash
# Basic run with config file
uv run src/run_evals.py --config config_files/your_config.yaml --name experiment_name

# The framework will:
# 1. Load parameters from config file (validated by master_params.py)
# 2. Pass them to select_task.py for execution
# 3. Save results organized by dataset and task
```

### Results Structure

The `ExperimentTracker` manages experiment data:
- Each experiment run generates a tracking CSV file stored in the results directory
- Results are organized by task and dataset: `results/<dataset>/<dataset>__<task>.csv`
- Each run gets a unique ID and stores metadata (timestamp, run name, file paths)
- Individual evaluation logs are saved as JSON files viewable in Inspect AI

### Analyzing Results

1. **Inspect AI Log Viewer**: JSON result files automatically open in VS Code's Inspect AI viewer
2. **Jupyter Notebooks**: Use notebooks in `playground/` for custom analysis
3. **ExperimentTracker API**: Load and analyze results programmatically

### Architecture Flow

1. **run_evals.py**: Entry point that processes config files
2. **select_task.py**: Receives parameters and executes appropriate evaluation
3. **master_params.py**: Validates all experiment parameters
4. **utils.py**: Helper functions for evaluation pipeline
5. **experiment_tracker.py**: Manages results storage and retrieval

### Development

For extending the framework:
- Add new tasks in `src/tasks/task_datasets/`
- Modify parameter validation in `master_params.py`
- Create analysis notebooks in `playground/` 