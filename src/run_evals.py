import argparse
import itertools
import os
import shutil
import subprocess
from typing import Literal
import csv

from inspect_ai import eval, score
from pydantic import ValidationError
from dotenv import load_dotenv
load_dotenv()

from src.master_params import RunParamsStore, UnloggedParams, get_own_fields, get_inherited_experiment_fields, ScoreParams, RunParams
from src.select_task import SelectTaskStore
from src.utils.utils import RESULTS_DIR, TEST_RESULTS_DIR, dummy_scorer
from src.utils.launch_utils import (
    load_config,
    configure_logging,
    prepare_output_dir,
    transform_config,
    get_log_filepath,
    get_next_folder_number,
    filter_log_by_sample_score,
)
from src.experiment_tracker import ExperimentTracker
from src.utils.plotting_utils import get_eval_logs_list

from inspect_ai.log import write_eval_log

def launch_script(args: argparse.Namespace, test: Literal["param_configs", "run_tasks"] | None = None):

    config = load_config(args.config)
    
    config = transform_config(config)

    #Set-up expeirment tracker
    if args.name == "test_tracker":
        base_tracker_path = TEST_RESULTS_DIR
    else:
        base_tracker_path = RESULTS_DIR
    tracker = ExperimentTracker(os.path.join(base_tracker_path, "experiment_tracker"))

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
            # shutil.rmtree(output_dir)
            exit()
        

    #Record parameters of different valid parameter configurations in a csv file
    parameter_spec = []

    # Run the valid parameter configruations
    for ind, combo in enumerate(valid_param_configurations):
        TaskFunc = SelectTaskStore[combo.task_name]

        # Get inherited fields as kwargs and own fields as task_specific_params
        generic_params = get_inherited_experiment_fields(combo)
        task_specific_params = get_own_fields(combo)


        if combo.task_name in RunParams.__annotations__['task_name'].__args__:
            eval_params = {
                "model": combo.model,
                "temperature": combo.temperature,
                "log_dir": os.path.join(output_dir, get_log_filepath(config=combo, struct=config["logdir_structure"])),
                "limit": combo.limit,
                "epochs": combo.num_epochs,
                "max_connections": 50,
            }

            if test == "run_tasks":
                eval_params['limit'] = 1
                eval_params['epochs'] = 1
                eval_params['model'] = "openai/gpt-4o-mini"


            evallog = eval(
                TaskFunc(
                    **generic_params,  # Unpack all inherited parameters as kwargs
                    task_specific_params=task_specific_params,  # Pass own fields as dictionary
                    eval_params=eval_params,
                ),
                **eval_params,
            )
            logfile_name = evallog[0].location.split("/")[-1]

            combo_dict = {k: v for k, v in combo.model_dump().items() if v is not None}
            combo_dict["previous_run"] = "NA"
            combo_dict["logfile_name"] = logfile_name
            combo_dict["id_file"] = ind
            parameter_spec.append(combo_dict)
            logger.info("Completed evaluation for task: %s", combo.task_name)

        elif combo.task_name in ScoreParams.__annotations__['task_name'].__args__:

            # Split log_src to get task_name and id (format: "task_name-id")
            log_src_parts = combo.log_src.rsplit("-", 1)  # Split from the right, only once
            task_name = log_src_parts[0]
            experiment_id = log_src_parts[1]
            log_dir = tracker.get("file_path", task_name=task_name, dataset_name=combo.dataset_name, id=experiment_id)
            evallog_list = get_eval_logs_list(log_dir)

            if combo.task_name == "baseline_thresholds":
                find_baseline = lambda log: log.eval.task_args['kwargs']['sandbag_type'] == "baseline"
                eval_log_list = [log for log in evallog_list if find_baseline(log)]; assert len(eval_log_list) == 1

            
            # score_params = TaskFunc()
            
            for j,log in enumerate(evallog_list):
                scorer = TaskFunc(**generic_params, task_specific_params=task_specific_params)
                filter_log_by_sample_score(log, filter=combo.sample_filter)

                log = score(log, scorers=scorer, action="append")


                new_log_path = os.path.join(output_dir, log.location.split("/")[-1])
                write_eval_log(log, new_log_path)
                logfile_name = new_log_path.split("/")[-1]

                combo_dict = {k: v for k, v in combo.model_dump().items() if v is not None}
                combo_dict["previous_run"] = task_name + "-" + experiment_id
                combo_dict["logfile_name"] = logfile_name
                combo_dict["id_file"] = ind * len(evallog_list) + j
                parameter_spec.append(combo_dict)
                logger.info("Completed evaluation for task: %s", combo.task_name)
        
        else:
            raise ValueError(f"Task name {combo.task_name} not supported")
        
        # # Add non-None values from combo to parameter_spec
        # combo_dict = {k: v for k, v in combo.model_dump().items() if v is not None}
        # combo_dict["logfile_name"] = logfile_name
        # parameter_spec.append(combo_dict)
        # logger.info("Completed evaluation for task: %s", combo.task_name)

    #Write parameter_specification_file to the output directory
    csv_path = os.path.join(output_dir, "parameter_specs.csv")
    all_keys = set()  # Get all unique keys from all dictionaries
    for spec in parameter_spec:
        all_keys.update(spec.keys())
    
    with open(csv_path, 'w', newline='') as csvfile:  # Write CSV with all keys as columns
        # Ensure id_file is present and comes first
        assert 'id_file' in all_keys, "id_file must be present in all parameter specs"
        fieldnames = ['id_file'] + sorted([k for k in all_keys if k != 'id_file'])
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for spec in parameter_spec:
            writer.writerow(spec)
    
    logger.info("Wrote parameter specifications to %s", csv_path)




    #Set-up expeirment tracker
    assert len(config["dataset_name"]) == 1 and len(config["task_name"]) == 1
    dataset_name = config["dataset_name"][0]
    task_name = config["task_name"][0]
    
    if args.name != "test":

        #Now move the output directory to the desired results directory.
        new_output_dir = os.path.join(base_tracker_path, f"log_files/{dataset_name}/{task_name}")
        run_id = get_next_folder_number(new_output_dir)
        new_output_dir = os.path.join(new_output_dir, f"{run_id}_{args.name}")
        shutil.move(output_dir, new_output_dir)

        #Add to tracker
        
        tracker.add(
            id=run_id,
            dataset_name=dataset_name,
            task_name=task_name,
            run_name=args.name,
            file_path=new_output_dir,
            notes=""
        )




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", required=True, help="Path to the YAML configuration file."
    )
    parser.add_argument("--name", required=True, help="Name of the experiment.")
    parser.add_argument("--copy_file", required=False, default=None, help="file to copy to the output directory.")
    args = parser.parse_args()
    launch_script(args)

