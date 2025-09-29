from inspect_ai.scorer import Scorer
from typing import Literal
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from src.utils.shared_prompts.detection.sandbagging_monitor import sandbagging_monitor
from src.tasks.mbpp.mbpp_utils.mbpp_utils import MBPP_UTILS_DIR
from src.tasks.mbpp.mbpp_reference_implementation.mbpp_reference import extract_output
from src.tasks.mbpp.mbpp_utils.mbpp_utils import error_template



def soln_only_message_processor(role: Literal["system", "user", "assistant", "tool_inputs", "tool_outputs"], text: str) -> str:
    if role == "assistant":
        return f"###SUBMIT###\n{extract_output(text)}\n###SUBMIT###"
    else:
        return text


def mbpp_detection(
    monitor_scale: Literal["binary", "ordinal"],
    visible_to_monitor: Literal["solution", "solution_stripped", "all"],
    flag_error: bool,
    model: str,
    max_tokens: int,
    include_checks: bool,
) -> Scorer:
    """Return sandbagging monitor scorer for mbpp dataset.

    Args:
        monitor_scale: The scale of the monitor.
        visible_to_monitor: The visibility of the monitor.
        flag_error: Whether to flag the error.
        model: The model to use to grade the solution.
        max_tokens: The maximum number of tokens to use to grade the solution.
        include_checks: Whether to include the checks.

    Returns:
        Scorer: The sandbagging_monitor scorer configured with mbpp-specific settings
    """

    if visible_to_monitor == "solution":
        output_message_processor = (["assistant"], soln_only_message_processor)
    elif visible_to_monitor == "solution_stripped":
        raise ValueError("Solution stripped is not supported for this scorer")
    else:
        output_message_processor = None

    error_constructor = error_template
    error_constructor["scorer_name"] = "verify"

    # Create and return the sandbagging_monitor scorer
    return sandbagging_monitor(
        monitor_scale=monitor_scale,
        visible_to_monitor=visible_to_monitor,
        flag_error=flag_error,
        model=model,
        max_tokens=max_tokens,
        include_checks=include_checks,
        error_constructor=error_constructor,
        dataset_prompts_dir=MBPP_UTILS_DIR,
        output_message_processor=output_message_processor,
    )



if __name__ == "__main__":
    from inspect_ai.log import read_eval_log, write_eval_log
    from inspect_ai import score
    import sys

    fpath = "/Users/RobertAdragna/Documents/MATS/evals_suite_new/src/tasks/mbpp/experiments/detection/2025-09-19T18-06-12+01-00_task_CnEyRr7o47jmggYXXMHjiR.eval"

    # Create the scorer with test parameters
    scorer = mbpp_detection(
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
