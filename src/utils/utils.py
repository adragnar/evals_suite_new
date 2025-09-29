from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Callable, Any
import anthropic
import os

from inspect_ai.solver import system_message, generate, Solver, TaskState
from inspect_ai.scorer import CORRECT, scorer, accuracy, stderr, Target, Score, Scorer

REPO_ROOT = "/Users/RobertAdragna/Documents/MATS/evals_suite_new"
RESULTS_DIR = f"{REPO_ROOT}/results"
TEST_RESULTS_DIR = f"{REPO_ROOT}/tests/results"


TRASH_LOGS_DIR = f"{REPO_ROOT}/tests/trash_logs"


#EXPERIMENT UTILS DIRS
DETECTION_UTILS_DIR = f"{REPO_ROOT}/src/utils/shared_prompts/detection"
GENERATE_EXPLOITS_UTILS_DIR = f"{REPO_ROOT}/src/utils/shared_prompts/generate_exploits"
GENERATE_EXECUTE_UTILS_DIR = f"{REPO_ROOT}/src/utils/shared_prompts/generate_execute"
ALL_EXPS_UTILS_DIR = f"{REPO_ROOT}/src/utils/shared_prompts/all_experiments"


def pprint_inspect_messages(message_list, desired_roles: List[str], msg_mod_fnc: Callable = lambda x, y: y) -> str:
    assert set(desired_roles) <= set(["assistant", "tool_outputs", "user", "system", "tool_inputs"])
    output = []
    for i, msg in enumerate(message_list):

        for msg_type in ['system', 'user', 'assistant']:
            if msg.role == msg_type and (msg_type in desired_roles):
                output.append(f"MESSAGE {i} - Role:{msg.role}")
                content = msg_mod_fnc(msg.role, msg.text)
                output.append(f"##BEGIN MESSAGE CONTENT##\n{content}\n##END MESSAGE CONTENT##")
        


        if msg.role == "assistant" and "tool_inputs" in desired_roles:
            if hasattr(msg, 'tool_calls') and msg.tool_calls is not None:
                for j, tool_call in enumerate(msg.tool_calls):
                    toolcall_input = "" if tool_call.function == "submit" else tool_call.view.content
                    content = msg_mod_fnc("tool_inputs", toolcall_input)
                    output.append(f"\nTool Call {j+1} of Type {tool_call.function} Made: \n ###BEGIN TOOL CALL INPUT###\n{content}\n###END TOOL CALL INPUT###")


        if msg.role == "tool" and "tool_outputs" in desired_roles:
            output.append(f"MESSAGE {i} - Role:{msg.role}")
            content = msg_mod_fnc(msg.role, msg.text)
            output.append(f"###BEGIN TOOL CALL OUTPUT###\n{content}\n###END TOOL CALL OUTPUT###")
        
        output.append("\n")
    return "\n".join(output)
    

class PromptRenderer:
    def __init__(self, dataset_prompt_dir = None, experiment_prompt_dir = None, task_prompt_dir = None, all_exps_prompts_dir = None):
        self.all_exps_prompts_dir = all_exps_prompts_dir
        self.dataset_prompt_dir = dataset_prompt_dir
        self.experiment_prompt_dir = experiment_prompt_dir
        self.task_prompt_dir = task_prompt_dir



    def get_load_and_format_filter(self, env: Environment):
        """Get the load and format filter needed to process singe brace parameters"""
        def load_and_format(template_name: str, params: dict = {}) -> str:
            """Load a template and format it with single-brace syntax."""
            # Use the environment's loader to get the template source
            source, _, _ = env.loader.get_source(env, template_name)
            # Apply single-brace formatting
            return format_template(source, params)
        return load_and_format

    def render_jinja_template(self, template_name: str, root_paths: List[str] = [], **kwargs) -> str:
        """Render a Jinja template with the given context"""

        env = Environment(loader=FileSystemLoader(root_paths + [pth for pth in [self.all_exps_prompts_dir, self.dataset_prompt_dir, self.experiment_prompt_dir, self.task_prompt_dir] if pth is not None]))
        env.filters['load_and_format'] = self.get_load_and_format_filter(env)

        template = env.get_template(template_name)
        rendered_prompt = template.render(**kwargs)

        return rendered_prompt

    def get_template_source(self, template_name: str, root_paths: List[str] = []) -> str | None:
        """Get the raw template source without rendering. Return None iof doesn't exist"""
        
        env = Environment(loader=FileSystemLoader(root_paths + [pth for pth in [self.dataset_prompt_dir, self.experiment_prompt_dir, self.task_prompt_dir] if pth is not None]))
        try:
            source, _, _ = env.loader.get_source(env, template_name)
        except Exception as e:
            return None
        return source




def dummy_solver() -> Solver | List[Solver]:
 
    return [
        system_message("hello there"),
        generate(),
    ]


@scorer(metrics=[accuracy()])
def dummy_scorer() -> Scorer:
    async def scorer(state: TaskState, target: Target) -> Score:


        #Score the result
        score = Score(
            value=CORRECT,
        )

        return score

    return scorer


def call_anthropic_api(messages, model: str = "claude-3-5-sonnet-20240620", max_tokens: int = 4000) -> str:
    """Call the Anthropic API to generate a response to a given prompt"""
    client = anthropic.Anthropic(
        api_key=os.getenv("ANTHROPIC_API_KEY")
    )

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages
    )

    # Parse the returned text and return structured data
    return message.content[0].text



def get_text_from_sample_input(sample_input: str | List[Any]) -> str:
    """Given a sample input object, return the text of the input"""

    if type(sample_input) is str:
        return sample_input
    elif type(sample_input) is list and len(sample_input) == 1:
        return sample_input[0].content
    else:
        raise ValueError(f"Invalid input type: {type(sample_input)}")





##UKAISI FORMAT TEMPLATE
import pprint
from string import Formatter
from textwrap import indent
from typing import Any


def format_template(
    template: str,
    params: dict[str, Any],
    skip_unknown: bool = True,
) -> str:
    """Format a template string, optionally preserving unknown placeholders.

    Args:
        template: A string containing {placeholders} to be formatted
        params: Dictionary of parameters to substitute into the template
        skip_unknown: If True, preserve unknown placeholders; if False, raise KeyError

    Returns:
        The formatted string with parameters substituted

    Examples:
        >>> format_template("Hello {name}!", {"name": "World"})
        'Hello World!'
        >>> format_template("Hello {name}!", {}, skip_unknown=True)
        'Hello {name}!'
    """

    class SafeFormatter(Formatter):
        def get_field(self, field_name: str, args: Any, kwargs: Any) -> Any:
            try:
                # Handle array indexing and nested attributes
                first, rest = (
                    field_name.split(".", 1)
                    if "." in field_name
                    else (field_name, None)
                )
                first = first.split("[")[0]  # Remove any array indexing for the check

                if first not in params and skip_unknown:
                    return "{" + field_name + "}", field_name

                obj = params.get(first)
                if obj is None and skip_unknown:
                    return "{" + field_name + "}", field_name

                return super().get_field(field_name, args, kwargs)
            except (AttributeError, KeyError, IndexError) as e:
                if skip_unknown:
                    return "{" + field_name + "}", field_name
                raise KeyError(f"Failed to format field '{field_name}'") from e

        def format_field(self, value: Any, format_spec: str) -> Any:
            try:
                return super().format_field(value, format_spec)
            except (ValueError, TypeError):
                if skip_unknown:
                    return "{" + str(value) + ":" + format_spec + "}"
                raise


    result = SafeFormatter().format(template, **params)

    return result