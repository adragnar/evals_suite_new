"""
Pytest configuration for run_evals tests.
"""

def pytest_addoption(parser):
    """Add command-line options for dataset_name and task_type."""
    parser.addoption(
        "--dataset_name",
        action="store",
        default="inference_server",
        help="Dataset name to use for testing"
    )
    parser.addoption(
        "--task_type",
        action="store",
        default="ability_difference",
        help="Task type to use for testing"
    )