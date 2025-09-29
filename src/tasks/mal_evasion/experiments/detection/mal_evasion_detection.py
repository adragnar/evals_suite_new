from inspect_ai import Task
from inspect_ai.model import GenerateConfig
from inspect_ai.solver import system_message, prompt_template, generate

import dotenv
dotenv.load_dotenv()

# Import from reference implementation
from src.tasks.mal_evasion.mal_evasion_reference_implementation.mal_evasion_reference import get_mal_evasion_dataset, malware_detection_evasion_score
from src.tasks.mal_evasion.mal_evasion_utils.mal_evasion_utils import error_template
from src.utils.shared_prompts.detection.sandbagging_monitor import sandbagging_monitor

# Import utilities
from src.utils.utils import PromptRenderer
from src.tasks.mal_evasion.mal_evasion_utils.mal_evasion_utils import MAL_EVASION_UTILS_DIR
from src.tasks.mal_evasion.mal_evasion_utils.mal_evasion_utils import error_template





def mal_evasion_detection(
    model: str,
    monitor_scale: str,
    visible_to_monitor: str,
    flag_error: bool,
    max_tokens: int,
    include_checks: bool,
) -> Task:
    """
    Create an InspectAI task for detecting sandbagging in malware evasion solutions.

    Args:
        log_src: Source of logs to analyze
        sample_filter: Filter to apply to samples
        model: Model to use for detection
        monitor_scale: Scale for monitoring ("binary" or "ordinal")
        visible_to_monitor: What's visible to monitor ("solution", "solution_stripped", "all")
        flag_error: Whether to flag errors
        max_tokens: Maximum tokens for response
        include_checks: Whether to include additional checks

    Returns:
        InspectAI Task object configured for sandbagging detection
    """
    
    if visible_to_monitor == "solution":
        output_message_processor = (["tool_inputs", "tool_outputs"], lambda x, y: y)
    elif visible_to_monitor == "solution_stripped":
        raise ValueError("Solution stripped is not supported for this scorer")
    else:
        output_message_processor = None


    error_constructor = error_template
    error_constructor["scorer_name"] = "malware_detection_evasion_score"

    # Create and return the sandbagging_monitor scorer
    return sandbagging_monitor(
        monitor_scale=monitor_scale,
        visible_to_monitor=visible_to_monitor,
        flag_error=flag_error,
        model=model,
        max_tokens=max_tokens,
        include_checks=include_checks,
        error_constructor=error_constructor,
        dataset_prompts_dir=MAL_EVASION_UTILS_DIR,
        output_message_processor=output_message_processor,
    )



if __name__ == "__main__":

    from inspect_ai.log import read_eval_log, write_eval_log
    from inspect_ai import score
    import sys

    fpath = "/Users/RobertAdragna/Documents/MATS/evals_suite_new/src/tasks/mal_evasion/experiments/detection/2025-09-29T17-13-17+01-00_select-task-generate-execute_F5QfuUZ8mRW34pt5WpUwee.eval"

    # Create the scorer with test parameters
    scorer = mal_evasion_detection(
        monitor_scale="binary",
        visible_to_monitor="solution",
        flag_error=True,
        model="openai/gpt-4o-mini",
        max_tokens=1000,
        include_checks=True
    )

    log = read_eval_log(fpath)

    # Score the log with our detection scorer
    scored_log = score(log, scorers=scorer, action="append")
    write_eval_log(scored_log, fpath)
