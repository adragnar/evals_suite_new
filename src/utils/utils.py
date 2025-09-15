from jinja2 import Environment, FileSystemLoader
from typing import List


REPO_ROOT = "/Users/RobertAdragna/Documents/MATS/evals_suite_new"
RESULTS_DIR = f"{REPO_ROOT}/results"
TEST_RESULTS_DIR = f"{REPO_ROOT}/tests/results"


TRASH_LOGS_DIR = f"{REPO_ROOT}/tests/trash_logs"




class PromptRenderer:
    def __init__(self, dataset_prompt_dir, experiment_prompt_dir):
        self.dataset_prompt_dir = dataset_prompt_dir
        self.experiment_prompt_dir = experiment_prompt_dir

    def render_jinja_template(self, template_name: str, root_paths: List[str] = [], **kwargs) -> str:
        """Render a Jinja template with the given context"""

        env = Environment(loader=FileSystemLoader(root_paths + [self.dataset_prompt_dir, self.experiment_prompt_dir]))

        template = env.get_template(template_name)
        rendered_prompt = template.render(**kwargs)

        return rendered_prompt
