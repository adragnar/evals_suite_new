import argparse
import itertools
import os
import shutil
import subprocess
from typing import Literal

from inspect_ai import eval
from pydantic import ValidationError
from dotenv import load_dotenv
load_dotenv()

from src.master_params import RunParamsStore, UnloggedParams, get_own_fields, get_inherited_experiment_fields
from src.select_task import SelectTaskStore
from src.utils.launch_utils import (
    load_config,
    configure_logging,
    prepare_output_dir,
    transform_config,
    get_log_filepath,
)


def launch_script(args: argparse.Namespace, test: Literal["param_configs", "run_tasks"] | None = None):

    config = load_config(args.config)
    
    config = transform_config(config)

    # Prepare the output directory
    output_dir = prepare_output_dir(config["log_dir"], args.name)
    logger = configure_logging(config["log_level"], output_dir)

    #Copy git_commit, config, all specified files to the output directory
    git_commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('ascii').strip()
    logger.info("Git commit: %s", git_commit)
    shutil.copy(args.config, os.path.join(output_dir, args.config.split("/")[-1]))
    if args.copy_file is not None:
        shutil.copy(args.copy_file, os.path.join(output_dir, args.copy_file.split("/")[-1]))


    # Ensure logging parameters are in config file
    assert UnloggedParams.issubset(set(config.keys()))

    # Generate all possible parameter combinations
    exp_config = {k: v for k, v in config.items() if k not in UnloggedParams}
    param_combinations = itertools.product(*exp_config.values())
    param_configurations = [
        dict(zip(exp_config.keys(), combo, strict=False))
        for combo in param_combinations
    ]

    # Generate the valid parameter configurations
    valid_param_configurations = []
    for configuration in param_configurations:
        ModelClass = RunParamsStore[configuration["dataset_name"]][configuration["task_name"]]
        try:
            combo = ModelClass.model_validate(configuration)
            valid_param_configurations.append(combo)
        except ValidationError as e:
            logger.error("Invalid configuration of parameters : %s", e)

    if test == "param_configs":
        shutil.rmtree(output_dir)
        return valid_param_configurations

    # Ask the user whether they want to proceed
    if test is None:
        proceed = (
            input(
                f"There are {len(valid_param_configurations)} experiments in this run. Did you expect this? (Y/N)"
            )
            .strip()
            .lower()
        )
        if proceed != "y":
            print("Aborting the execution.")
            shutil.rmtree(output_dir)
            exit()
        
    # Run the valid parameter configruations
    
    for combo in valid_param_configurations:
        TaskFunc = SelectTaskStore[combo.task_name]

        # Get inherited fields as kwargs and own fields as task_specific_params
        generic_params = get_inherited_experiment_fields(combo)
        task_specific_params = get_own_fields(combo)
        eval_params = {
            "model": combo.model,
            "temperature": combo.temperature,
            "log_dir": os.path.join(output_dir, combo.model.split("/")[-1], get_log_filepath(config=combo, struct=config["logdir_structure"])),
            "limit": combo.limit,
            "epochs": combo.num_epochs,
            "max_connections": 50,
        }

        if test == "run_tasks":
            eval_params['limit'] = 1
            eval_params['epochs'] = 1
            eval_params['model'] = "openai/gpt-4o-mini"


        eval(
            TaskFunc(
                **generic_params,  # Unpack all inherited parameters as kwargs
                task_specific_params=task_specific_params,  # Pass own fields as dictionary
                eval_params=eval_params,
            ),
            **eval_params,
        )

        logger.info("Completed evaluation for task: %s", combo.task_name)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", required=True, help="Path to the YAML configuration file."
    )
    parser.add_argument("--name", required=True, help="Name of the experiment.")
    parser.add_argument("--copy_file", required=False, default=None, help="file to copy to the output directory.")
    args = parser.parse_args()
    launch_script(args)

