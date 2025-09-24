"""
Test suite for inference_server ability_difference task configuration and parameter passing.
"""

import sys
from pathlib import Path
import pytest
import argparse
import threading
import json
from typing import List

from dotenv import load_dotenv
load_dotenv()

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
from src.run_evals import launch_script


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


@pytest.fixture
def dataset_name(request):
    """Fixture to get dataset_name from command line."""
    return request.config.getoption("--dataset_name")


@pytest.fixture
def task_type(request):
    """Fixture to get task_type from command line."""
    return request.config.getoption("--task_type")



# Configuration test cases - used for BOTH tests
def get_configs(task_type, dataset_name) -> List[dict]:
    """Gets all configuration files for a given task_type & dataset"""
    fdir = Path(__file__).parent
    configs_path = f"{fdir}/test_config_files/{dataset_name}/{task_type}/config_info.jsonl"

    with open(configs_path, "r") as f:
        configs = [json.loads(line) for line in f]

    return configs





class TestConfigurationCount:
    """Test that configurations generate the expected number of valid parameter combinations."""
    
    def test_configuration_counts(self, task_type, dataset_name):
        """Test each configuration file produces the expected number of valid combinations."""
        configs = get_configs(task_type, dataset_name)

        for config in configs:
            args = argparse.Namespace(config=config["file"], name="test", copy_file=None)
            
            param_configurations = launch_script(args, test="param_configs")


            assert len(param_configurations) == config["expected_count"], (
                f"Configuration {config['name']} produced {len(param_configurations)} valid combinations, "
                f"expected {config['expected_count']}."
            )
    

    def test_log_runs(self, task_type, dataset_name):
        """Smoke test that the experiment runs without errors"""
        configs = get_configs(task_type, dataset_name)

        for config in configs:
            args = argparse.Namespace(config=config["file"], name="test", copy_file=None)

            if config["should_pass"] and config["smoke_test"]:
                # Test passes if launch_script either completes successfully or runs for at least 10 seconds
                result = {"completed": False, "error": None}
                
                def run_launch_script():
                    try:
                        launch_script(args, test="run_tasks")
                        result["completed"] = True
                    except Exception as e:
                        result["error"] = e
                
                # Start the launch_script in a separate thread
                thread = threading.Thread(target=run_launch_script)
                thread.daemon = True
                thread.start()
                
                # Wait for either completion or 10 seconds
                thread.join(timeout=10.0)
                
                # Test passes if either:
                # 1. The script completed successfully (thread finished and no error)
                # 2. The script is still running after 10 seconds (thread is still alive)
                if result["completed"] and result["error"] is None:
                    # Script completed successfully
                    pass
                elif thread.is_alive():
                    # Script is still running after 10 seconds - this indicates it's working properly
                    pass
                else:
                    # Script completed with an error within 10 seconds
                    if result["error"] is not None:
                        raise result["error"]
                    else:
                        # Script completed but something unexpected happened
                        pytest.fail(f"Script for {config['name']} completed unexpectedly without error or success")
                





if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])