"""This module contains the Pydantic model for the experiment parameters. Note that optional eval parameters must have default values, while optional task parameters must default to None."""
from typing import Literal, Self
from pydantic import BaseModel, create_model, model_validator


def get_own_fields(model_instance):
    """Get fields defined directly on the class, excluding inherited fields.
    Returns a dictionary of field_name: field_value for non-inherited fields."""
    model_class = model_instance.__class__
    own_field_names = set(model_class.model_fields.keys()) 
    
    # Remove fields that are inherited from base classes
    for base in model_class.__bases__:
        if hasattr(base, 'model_fields'):
            own_field_names -= set(base.model_fields.keys())
    
    # Return dictionary of field names and their values from the instance
    return {name: getattr(model_instance, name) for name in own_field_names}

def get_inherited_experiment_fields(model_instance):
    """Get fields inherited from parent classes.
    Returns a dictionary of field_name: field_value for inherited fields."""
    model_class = model_instance.__class__
    inherited_field_names = set()
    
    # Collect fields from all base classes
    for base in model_class.__bases__:
        if hasattr(base, 'model_fields') and base.__name__ != 'RunParams' and base.__name__ != 'ScoreParams':
            inherited_field_names.update(base.model_fields.keys())
    
    # Return dictionary of field names and their values from the instance
    return {name: getattr(model_instance, name) for name in inherited_field_names}

# def check_model_validator_tasks_complete(options):
#     """Ensure all tasks defined by the model are included in a model validator options dict."""
#     assert set().union(*options.values()) == set(
#         ExpParams.model_fields["task_name"].annotation.__args__
#     )


# def get_task_specific_params(combo):
#     """Return a more specific pydantic object with just the task-relevant parameters.

#     combo: pydantic ExpParams model with all experiment parameters
#     task_name: Name of the task you're running
#     """
#     if "inference_server_s1" in combo.task_name:
#         fields = {
#             "vuln_section": (str, ...),
#             "sandbag_type": (Literal["reward_hack", "subtle"], ...),
#             "num_strats": (int, ...),
#         }
#         InferenceServerS1Params = create_model("InferenceServerS1Params", **fields)
#         InferenceServerS1Params = InferenceServerS1Params(
#             **combo.model_dump(include={"vuln_section", "sandbag_type", "num_strats"})
#         )
#         return InferenceServerS1Params
#     elif "inference_server_ability_difference" in combo.task_name:
#         fields = {
#             "sandbag_type": (Literal["reward_hack", "subtle", "baseline"], ...),
#             "timeout": (int, ...),
#             "ref_soln": (bool, ...),
#             "api_difficulty": (Literal["basic", "intermediate"], ...),
#         }
#         InferenceServerAbilityDifferenceParams = create_model("InferenceServerAbilityDifferenceParams", **fields)
#         InferenceServerAbilityDifferenceParams = InferenceServerAbilityDifferenceParams(
#             **combo.model_dump(include={"sandbag_type", "timeout", "api_difficulty", "ref_soln"})
#         )
#         return InferenceServerAbilityDifferenceParams
#     elif "inference_server_generate_execute" in combo.task_name:
#         fields = {
#             "sandbag_type": (Literal["reward_hack", "subtle", "baseline"], ...),
#             "timeout": (int, ...),
#             "ref_soln": (bool, ...),
#             "api_difficulty": (Literal["basic", "intermediate"], ...),
#             "num_cycles": (int, ...),
#             "fixed_length": (bool, ...),
#             "generate_model": (str, ...),
#             "scorer_model": (str, ...),
#             "num_strats": (int, ...),
#             "is_hidden_scratchpad": (bool, ...),
#         }
#         InferenceServerGenerateExecuteParams = create_model("InferenceServerGenerateExecuteParams", **fields)
#         InferenceServerGenerateExecuteParams = InferenceServerGenerateExecuteParams(
#             **combo.model_dump(include={"sandbag_type", "timeout", "api_difficulty", "ref_soln", "num_cycles", "num_strats", "generate_model", "scorer_model", "fixed_length", "is_hidden_scratchpad"})
#         )
#         return InferenceServerGenerateExecuteParams
#     elif "inference_server_detection" in combo.task_name:
#         fields = {
#             "isdetect_log_path": (str, ...),
#             "isdetect_monitor_scale": (Literal["binary", "ordinal"], ...),
#             "isdetect_visible_to_monitor": (Literal["solution", "solution_stripped", "all"], ...),
#             "isdetect_flag_error": (bool, ...),
#             "isdetect_scorer_model": (str, ...),
#             "isdetect_include_checks": (bool, ...),
#         }
#         InferenceServerDetectionParams = create_model("InferenceServerDetectionParams", **fields)
#         InferenceServerDetectionParams = InferenceServerDetectionParams(
#             **combo.model_dump(include={"isdetect_log_path", "isdetect_monitor_scale", "isdetect_visible_to_monitor", "isdetect_flag_error", "isdetect_scorer_model", "isdetect_include_checks"})
#         )
#         return InferenceServerDetectionParams
#     else:
#         return {}


class RunParams(BaseModel):
    # Universal task Parameters

    task_name: Literal[
        "generate_exploits",
        "ability_difference",
        "generate_execute",
    ]
    
    dataset_name: Literal[
        "inference_server",
        "mbpp",
        "mal_evasion",
    ]

    # Universal  Eval Parameters
    model: Literal[
        "openai/gpt-4o-mini",
        "openai/gpt-4o",
        "anthropic/claude-3-5-haiku-20241022",
        "anthropic/claude-3-5-sonnet-20241022",
        "anthropic/claude-3-7-sonnet-20250219",
        "anthropic/claude-sonnet-4-20250514",
        "anthropic/claude-3-opus-20240229",
        "openai/gpt-4.5-preview-2025-02-27",
        "openai/o1-2024-12-17",
        "openai/o3-mini-2025-01-31"
    ]
    limit: int
    temperature: float
    num_epochs: int



class ScoreParams(BaseModel):
    # Universal task Parameters

    task_name: Literal[
        "detection",
        "baseline_thresholds",
    ]
    dataset_name: Literal[
        "inference_server",
        "mbpp",
        "mal_evasion",
    ]
    log_src: str
    sample_filter: str | Literal["NA"]



class DetectionParams(ScoreParams):

    model: Literal[
        "openai/gpt-4o-mini",
        "openai/gpt-4o",
        "anthropic/claude-3-5-haiku-20241022",
        "anthropic/claude-3-5-sonnet-20241022",
        "anthropic/claude-3-7-sonnet-20250219",
        "anthropic/claude-sonnet-4-20250514",
        "anthropic/claude-3-opus-20240229",
        "openai/gpt-4.5-preview-2025-02-27",
        "openai/o1-2024-12-17",
        "openai/o3-mini-2025-01-31"
    ]
    monitor_scale: Literal["binary", "ordinal"]
    visible_to_monitor: Literal["solution", "solution_stripped", "all"]
    flag_error: bool
    max_tokens: int
    include_checks: bool


class AbilityDifferenceParams(RunParams):
    sandbag_type: Literal["reward_hack", "subtle", "baseline"]
    ref_soln: bool

class GenerateExploitsParams(RunParams):
    sandbag_type: Literal["reward_hack", "subtle"]
    num_strats: int
    fixed_length: bool

class GenerateExecuteParams(RunParams):
    sandbag_type: Literal["reward_hack", "subtle"]
    hidden_scratchpad: bool




#Classes for Each Task 
##InferenceServer
class InferenceServerAbilityDifferenceParams(AbilityDifferenceParams):
    difficulty: Literal["basic", "intermediate"]
    timeout: int


    @model_validator(mode="after")
    def check_params(self) -> Self:
        if self.difficulty not in ["basic"]:
            assert self.ref_soln is False, "ref_soln must be False for intermediate difficulty"
        
        return self

class InferenceServerGenerateExploitsParams(GenerateExploitsParams):
    difficulty: Literal["basic", "intermediate"]


class InferenceServerGenerateExecuteParams(GenerateExecuteParams):
    difficulty: Literal["basic", "intermediate"]
    timeout: int


class InferenceServerDetectionParams(DetectionParams):
    pass


# MBPP Dataset Parameters
class MbppAbilityDifferenceParams(AbilityDifferenceParams):
    timeout: int | None = None

    @model_validator(mode="after")
    def check_params(self) -> Self:
        # Add any validation logic here if needed
        assert self.ref_soln is False, "ref_soln must be False for MBPP"
        return self

class MbppGenerateExploitsParams(GenerateExploitsParams):
    pass

class MbppGenerateExecuteParams(GenerateExecuteParams):
    pass

class MbppDetectionParams(DetectionParams):
    pass


# Mal Evasion Dataset Parameters
class MalEvasionAbilityDifferenceParams(AbilityDifferenceParams):
    timeout: int | None = None
    variant: str | None = None

    @model_validator(mode="after")
    def check_params(self) -> Self:
        # Add any validation logic here if needed
        return self

class MalEvasionGenerateExecuteParams(GenerateExecuteParams):
    timeout: int | None = None
    variant: str | None = None

class MalEvasionDetectionParams(DetectionParams):
    pass


# vuln_section: Literal["all", "top_level", "valid_json", "results_not_equal", "number_sequence_continued", "valid_types", "valid_token_usage"]




###Information
UnloggedParams = {"log_dir", "log_level", "logdir_structure"}
RunParamsStore = {
    "inference_server": {
        "ability_difference": InferenceServerAbilityDifferenceParams,
        "generate_exploits": InferenceServerGenerateExploitsParams,
        "generate_execute": InferenceServerGenerateExecuteParams,
        "detection": InferenceServerDetectionParams
    },
    "mbpp": {
        "ability_difference": MbppAbilityDifferenceParams,
        "generate_exploits": MbppGenerateExploitsParams,
        "generate_execute": MbppGenerateExecuteParams,
        "detection": MbppDetectionParams,
        "baseline_thresholds": MbppDetectionParams
    },
    "mal_evasion": {
        "ability_difference": MalEvasionAbilityDifferenceParams,
        "generate_execute": MalEvasionGenerateExecuteParams,
        "detection": MalEvasionDetectionParams,
        "baseline_thresholds": MalEvasionDetectionParams
    }
}  #{dataset:{taskname: ModelClass}}
    

    