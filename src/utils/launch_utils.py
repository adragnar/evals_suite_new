import os
import re
from pathlib import Path
import argparse

import logging
from datetime import datetime
from pathlib import Path
import yaml

from inspect_ai.scorer import scorer, Score, Target, CORRECT
from inspect_ai.solver import TaskState

def load_config(config_path):
    # Specify to convert "None" str values to Nonetype
    def none_constructor(loader, node):
        if isinstance(node, yaml.ScalarNode) and node.value == "None":
            return None
        return loader.construct_scalar(node)

    class CustomLoader(yaml.SafeLoader):
        pass

    CustomLoader.add_constructor("tag:yaml.org,2002:str", none_constructor)

    # Load the data
    with open(config_path) as file:
        config = yaml.load(file, Loader=CustomLoader)

    return config


def configure_logging(log_level, log_dir):
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(os.path.join(log_dir, "script.log"), mode="a")],
    )
    logger = logging.getLogger(__name__)
    logger.info("Logging initialized at %s level", log_level)
    return logger


def prepare_output_dir(log_dir, name):
    """Create a timestamped output directory for logs."""
    next_folder_number = get_next_folder_number(log_dir)
    project_root = find_project_root(Path(__file__).resolve())
    timestamp = f"{next_folder_number}_" + datetime.now().strftime("%M_%H-%d-%m")

    # Generate log directory
    output_dir = os.path.join(project_root, log_dir, f"{timestamp}_{name}")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def find_project_root(start: Path, marker_names=("pyproject.toml", ".git")) -> Path:
    current = start.resolve()
    while current != current.root:
        if any((current / marker).exists() for marker in marker_names):
            return current
        current = current.parent
    return start


def transform_config(config: dict) -> dict:
    """Adjust the arguments for a given task name to be different for particualr tasks"""
    from inspect_ai.log import list_eval_logs
   
    assert len(config["task_name"]) == 1, "Only one task name is supported"

    if config["task_name"][0] == "inference_server_detection":
        dir_list = []
        for log_info in list_eval_logs(config["isdetect_log_path"][0]):
            dir_list.append(log_info.name[7:])
        config["isdetect_log_path"] = dir_list 

    return config




########################################################
################# Helper Functions  ##################
########################################################

def get_next_folder_number(log_dir: str) -> int:
    # Get all items in the base path
    script_path = Path(__file__).resolve()
    project_root = find_project_root(script_path)
    base_path = os.path.join(project_root, log_dir)
    print(base_path)

    if not os.path.exists(base_path):
        return 1
    items = os.listdir(base_path)

    # Filter to keep only directories
    dirs = [d for d in items if os.path.isdir(os.path.join(base_path, d))]

    # This regex will capture leading digits at the start of a string
    leading_digits_pattern = re.compile(r"^(\d+)")

    # Extract integer prefixes
    numeric_prefixes = []
    for d in dirs:
        match = leading_digits_pattern.match(d)
        if match:
            numeric_prefixes.append(int(match.group(1)))

    # If there are no existing numbered folders, we start at 1
    if not numeric_prefixes:
        next_number = 1
    else:
        next_number = max(numeric_prefixes) + 1

    return next_number


def get_log_filepath(config, struct: str) -> str:
    '''Input; combo object with parameters as attributes and a string with mutliple parameters in the config file seperated by dashes'''

    if struct == "":
        return ""
    else:
        struct_params = struct.split("-")
        fpath = ""
        
        for param in struct_params:
            assert hasattr(config, param), f"Parameter {param} not found in config"
            fpath = os.path.join(fpath, f"{param}={getattr(config, param)}")

    return fpath





