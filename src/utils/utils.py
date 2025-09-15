from jinja2 import Environment, FileSystemLoader
from typing import List


from inspect_ai.solver import system_message, generate, Solver

REPO_ROOT = "/Users/RobertAdragna/Documents/MATS/evals_suite_new"
RESULTS_DIR = f"{REPO_ROOT}/results"
TEST_RESULTS_DIR = f"{REPO_ROOT}/tests/results"


TRASH_LOGS_DIR = f"{REPO_ROOT}/tests/trash_logs"




class PromptRenderer:
    def __init__(self, dataset_prompt_dir = None, experiment_prompt_dir = None, task_prompt_dir = None):
        self.dataset_prompt_dir = dataset_prompt_dir
        self.experiment_prompt_dir = experiment_prompt_dir
        self.task_prompt_dir = task_prompt_dir

    def render_jinja_template(self, template_name: str, root_paths: List[str] = [], **kwargs) -> str:
        """Render a Jinja template with the given context"""

        env = Environment(loader=FileSystemLoader(root_paths + [pth for pth in [self.dataset_prompt_dir, self.experiment_prompt_dir, self.task_prompt_dir] if pth is not None]))

        template = env.get_template(template_name)
        rendered_prompt = template.render(**kwargs)

        return rendered_prompt


def dummy_solver() -> Solver | List[Solver]:
 
    return [
        system_message("hello there"),
        generate(),
    ]