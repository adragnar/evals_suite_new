

from pathlib import Path
from typing import Literal
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
import csv
import os


from inspect_ai import Task, task
from inspect_ai.dataset import Sample, MemoryDataset
from inspect_ai.scorer import (
    CORRECT,
    INCORRECT,
    Score,
    Scorer,
    Target,
    accuracy,
    scorer,
    stderr,
)
from inspect_ai.solver import (
    Solver,
    TaskState,
    system_message,
    prompt_template,
    generate,
    solver,
    Generate,
    user_message,
)
from inspect_ai.model._chat_message import ChatMessageSystem

from inspect_ai.tool import bash, python
from inspect_ai.util import sandbox
from inspect_ai.solver import basic_agent
from pydantic import BaseModel

from src.utils.utils import call_anthropic_api
from src.utils.utils import PromptRenderer, GENERATE_EXECUTE_UTILS_DIR, ALL_EXPS_UTILS_DIR

from src.utils.shared_prompts.generate_exploits.generate_exploits import generate_vulnerabilities_solver


def generate_execute_solver(
    sandbag_type: str,
    hidden_scratchpad: bool,
    dataset_prompt_dir: str = None,
    experiment_prompt_dir: str = None,
) -> Solver:

    solver = generate_vulnerabilities_solver(sandbag_type=sandbag_type, num_strats=1, fixed_length=True, dataset_prompt_dir=dataset_prompt_dir)


    prompt_renderer = PromptRenderer(dataset_prompt_dir=dataset_prompt_dir, task_prompt_dir=GENERATE_EXECUTE_UTILS_DIR, all_exps_prompts_dir=ALL_EXPS_UTILS_DIR)
    execute_vuln_prompt = prompt_renderer.render_jinja_template(
        "exec_vulns_system_prompt.jinja2",
        sandbag_type=sandbag_type,
        hidden_scratchpad=hidden_scratchpad,
    )

    solver = solver + [restart_to_execute(execute_vuln_prompt), user_message(prompt_renderer.render_jinja_template("exec_vulns_user_prompt.jinja2")), generate()]
    return solver



@solver
def restart_to_execute(template: str):
    """Custom solver that deletes all messages from the task state and saves the last assistant message."""
    async def solve(state: TaskState, generate: Generate) -> TaskState:
        # Save the last assistant message text to sample metadata before clearing
        if state.messages and len(state.messages) > 0:
            # Save to sample metadata so it can be used in prompt_template
            state.metadata["vulnerability_text"] = state.messages[-1].content

        # Clear all messages from the state
        state.messages = []
        

        # Format the template with both values
        # kwargs = {"prompt": state.input}


        # kwargs = omit(state.metadata | state.store._data, ["prompt"]) | params
        # prompt.text = format_template(prompt_template, {"prompt": prompt.text} | kwargs)
        formatted_prompt = template.format(
            vulnerability_text=state.metadata["vulnerability_text"],
        )

        # # Add as a user message
        # from inspect_ai.solver import user_message
        state.messages.append(ChatMessageSystem(content=formatted_prompt))
        return state

    return solve