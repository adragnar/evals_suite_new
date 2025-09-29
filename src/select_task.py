"""Task Selection Module.

This module provides functionality to select and configure various evaluation tasks based on configuration parameters.
"""

from typing import Any, Protocol

from inspect_ai import task
from src.master_params import RunParams, ScoreParams



def return_task(task_library, kwargs, task_specific_params, base_pydantic_class=RunParams):
    task_func = task_library.get(kwargs.get('dataset_name'))
    kwargs = {k: v for k, v in kwargs.items() if k not in base_pydantic_class.model_fields}
    return task_func(**kwargs, **task_specific_params)

def return_scorer(scorer_library, kwargs, task_specific_params):
    """Return a scorer function for detection tasks.

    Similar to return_task but handles scorer functions that return Scorer objects.
    """
    scorer_func = scorer_library.get(kwargs.get('dataset_name'))
    # Don't filter kwargs for scorers - pass all inherited params
    # Pass task_specific_params as individual keyword arguments
    return scorer_func(**task_specific_params, **kwargs)

@task
def select_task_generate_exploits(
    task_specific_params,
    eval_params,
    **kwargs,  # Accepts all inherited parameters
) -> Any:
    from src.tasks.task_datasets.inspect_evals.inference_server.generate_s1.src.s1 import inference_server_brainstorm_vulnerabilities
    from src.tasks.mbpp.experiments.generate_exploits.mbpp_generate_exploits import mbpp_generate_exploits

    task_library = {  # {dataset_name: task_func}
        "inference_server": inference_server_brainstorm_vulnerabilities,
        "mbpp": mbpp_generate_exploits,
    }

    return return_task(task_library, kwargs, task_specific_params)
    


@task
def select_task_ability_difference(
    task_specific_params,
    eval_params,
    **kwargs,  # Accepts all inherited parameters
) -> Any:
    from src.tasks.task_datasets.inspect_evals.inference_server.ability_difference.src.ability_difference import inference_server_ability_difference
    from src.tasks.mbpp.experiments.ability_difference.mbpp_ability_difference import mbpp_ability_difference
    from src.tasks.mal_evasion.experiments.ability_difference.mal_evasion_ability_difference import mal_evasion_ability_difference

    task_library = {  # {dataset_name: task_func}
        "inference_server": inference_server_ability_difference,
        "mbpp": mbpp_ability_difference,
        "mal_evasion": mal_evasion_ability_difference,
    }

    return return_task(task_library, kwargs, task_specific_params)
    

@task
def select_task_generate_execute(
    task_specific_params,
    eval_params,
    **kwargs,  # Accepts all inherited parameters
) -> Any:
    from src.tasks.task_datasets.inspect_evals.inference_server.generate_execute.src.generate_execute import inference_server_generate_execute
    from src.tasks.mbpp.experiments.generate_execute.mbpp_generate_execute import mbpp_generate_execute

    task_library = {  # {dataset_name: task_func}
        "inference_server": inference_server_generate_execute,
        "mbpp": mbpp_generate_execute,
    }

    return return_task(task_library, kwargs, task_specific_params)
    


def select_task_detection(
    task_specific_params,
    **kwargs,  # Accepts all inherited parameters
) -> Any:
    # from src.tasks.task_datasets.inspect_evals.inference_server.detection.src.detect_sandbagging import inference_server_detection
    from src.tasks.mbpp.experiments.detection.mbpp_detection import mbpp_detection

    task_library = {  # {dataset_name: task_func}
        # "inference_server": inference_server_detection,
        "mbpp": mbpp_detection,
    }

    return return_task(task_library=task_library, kwargs=kwargs, task_specific_params=task_specific_params, base_pydantic_class=ScoreParams)


## Define a base protocol for all tasks
class BaseTask(Protocol):
    def __call__(self, task_specific_params, eval_params):
        ...

## Define arguments for each task inheriting from BaseTask

class AbilityDifference(BaseTask):
    def __call__(self, sandbag_type: str, ref_soln: bool, task_specific_params, eval_params):
        ...

class GenerateExecute(BaseTask):
    def __call__(self, sandbag_type: str, num_strats: int, num_cycles: int, fixed_length: bool, is_hidden_scratchpad: bool, generate_model: str, scorer_model: str, max_tokens: int, task_specific_params, eval_params):
        ...

class Detection(BaseTask):
    def __call__(self, log_path: str, monitor_scale: str, visible_to_monitor: str, flag_error: bool, include_checks: bool, scorer_model: str, max_tokens: int, task_specific_params):
        ...

class GenerateExploits(BaseTask):
    def __call__(self, sandbag_type: str, num_strats: int, num_cycles: int, fixed_length: bool, generate_model: str, max_tokens: int, output_dir: str, task_specific_params, eval_params):
        ...
        ...

operations_ability_difference: list[AbilityDifference] = [select_task_ability_difference]
operations_generate_execute: list[GenerateExecute] = [select_task_generate_execute]
operations_detection: list[Detection] = [select_task_detection]
operations_generate_exploits: list[GenerateExploits] = [select_task_generate_exploits]



SelectTaskStore = {
    "ability_difference": select_task_ability_difference,
    "generate_execute": select_task_generate_execute,
    "detection": select_task_detection,
    "baseline_thresholds": select_task_detection,
    "generate_exploits": select_task_generate_exploits
}