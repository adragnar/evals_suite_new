"""
Experiment Tracker for managing experiment runs across different datasets and tasks.
"""

import csv
import shutil
from pathlib import Path
from typing import Dict, List
from datetime import datetime


class ExperimentTracker:
    """
    Manages experiment tracking across different datasets and tasks.

    Each dataset/task combination has its own table stored as a CSV file.
    """

    # Define task-specific dependency columns
    TASK_DEPENDENCIES = {
        "generate_execute": [],
        "detection": ["generate_id", "execute_id"],
        "ability_difference": [],  # No dependencies for ability_difference
        "generate_exploits": []  # No dependencies for generate_exploits
    }

    def __init__(self, base_dir):
        """
        Initialize the ExperimentTracker.

        Args:
            base_dir: Base directory for storing experiment data. Has form <dataset_name>/<task_name>
        """

        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _get_table_path(self, dataset_name: str, task_name: str) -> Path:
        """Get the path to the table file for a dataset/task combination."""
        dataset_dir = self.base_dir / dataset_name
        dataset_dir.mkdir(parents=True, exist_ok=True)
        # Use double underscore format for filename
        return dataset_dir / f"{dataset_name}__{task_name}.csv"

    def _get_columns(self, task_name: str) -> List[str]:
        """Get the column names for a specific task."""
        base_columns = ['id', 'run_name', 'notes', 'file_path', 'timestamp']
        if task_name in self.TASK_DEPENDENCIES:
            base_columns.extend(self.TASK_DEPENDENCIES[task_name])
        return base_columns

    def _load_table(self, dataset_name: str, task_name: str) -> List[Dict]:
        """Load the experiment table for a dataset/task combination."""
        table_path = self._get_table_path(dataset_name, task_name)

        if table_path.exists():
            with open(table_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                return list(reader)
        return []

    def _save_table(self, dataset_name: str, task_name: str, table: List[Dict]):
        """Save the experiment table for a dataset/task combination."""
        table_path = self._get_table_path(dataset_name, task_name)

        if not table:
            # If table is empty, still create the file with headers
            columns = self._get_columns(task_name)
            with open(table_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
        else:
            # Get all possible columns from the data
            all_columns = set()
            for entry in table:
                all_columns.update(entry.keys())

            # Ensure base columns are first
            base_columns = self._get_columns(task_name)
            ordered_columns = base_columns + [col for col in all_columns if col not in base_columns]

            with open(table_path, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=ordered_columns)
                writer.writeheader()
                writer.writerows(table)

    def _get_next_id(self, dataset_name: str, task_name: str) -> int:
        """Get the next available ID for a dataset/task combination."""
        table = self._load_table(dataset_name, task_name)

        if not table:
            return 0

        # Convert id strings to integers before finding max
        return max(int(entry['id']) for entry in table) + 1

    def add(self,
            dataset_name: str,
            task_name: str,
            run_name: str,
            file_path: str,
            id: int,
            notes: str = "",
            **kwargs) -> int:
        """
        Add a new experiment run to the database.

        Args:
            dataset_name: Name of the dataset
            task_name: Name of the task
            run_name: Name given to the experiment run
            file_path: Path to the log files for this experiment
            id: Experiment ID (mandatory, duplicates allowed)
            notes: Optional notes about the experiment
            **kwargs: Additional task-specific fields (e.g., generate_id, execute_id)

        Returns:
            The ID of the newly added experiment
        """
        table = self._load_table(dataset_name, task_name)

        # Use the provided ID (duplicates are allowed)
        experiment_id = id

        # Create the experiment entry
        entry = {
            'id': experiment_id,
            'run_name': run_name,
            'timestamp': datetime.now().isoformat(),
            'file_path': file_path,
            'notes': notes,
        }

        # Add task-specific dependency fields
        if task_name in self.TASK_DEPENDENCIES:
            for dep_field in self.TASK_DEPENDENCIES[task_name]:
                if dep_field in kwargs:
                    entry[dep_field] = kwargs[dep_field]
                else:
                    entry[dep_field] = None  # Set to None if not provided

        # Add any additional custom fields
        for key, value in kwargs.items():
            if key not in entry:
                entry[key] = value

        # Append to table and save
        table.append(entry)
        self._save_table(dataset_name, task_name, table)

        print(f"Added experiment {experiment_id} to {dataset_name}/{task_name}")
        return experiment_id

    def delete(self, dataset_name: str, task_name: str, run_name: str) -> bool:
        """
        Delete an experiment run from the database and remove associated log files.

        Args:
            dataset_name: Name of the dataset
            task_name: Name of the task
            run_name: Name of the experiment run to delete

        Returns:
            True if deletion was successful, False otherwise
        """
        table = self._load_table(dataset_name, task_name)

        # Find the experiment to delete
        experiment_to_delete = None
        for entry in table:
            if entry['run_name'] == run_name:
                experiment_to_delete = entry
                break

        if experiment_to_delete is None:
            print(f"Experiment with run_name '{run_name}' not found in {dataset_name}/{task_name}")
            return False

        # Delete associated log files if they exist
        file_path = experiment_to_delete.get('file_path')
        if file_path:
            full_path = Path(file_path)
            if full_path.exists():
                if full_path.is_dir():
                    shutil.rmtree(full_path)
                    print(f"Deleted directory: {full_path}")
                else:
                    full_path.unlink()
                    print(f"Deleted file: {full_path}")
            else:
                print(f"Warning: File path {full_path} does not exist")

        # Remove from table
        table = [entry for entry in table if entry['run_name'] != run_name]
        self._save_table(dataset_name, task_name, table)

        print(f"Deleted experiment '{run_name}' from {dataset_name}/{task_name}")
        return True