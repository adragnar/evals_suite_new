from typing import Literal
from inspect_ai import Task


def toy_mcqa_ability_difference(
    sandbag_type: str,
    dataset_name: Literal["mmlu-bio"],
    show_monitor: Literal["no_monitor", "solution", "all"],
    num_vulns: int,
    allowed_vulns: str,
    vuln_type: Literal["expression", "answer"],
    is_impossible_task: bool,
) -> Task:
    pass


    assert len(allowed_vulns.split('-')) == num_vulns




def get_scorer(included_vulns: list[str]):
    """From a list of included vulns, return a regex that includes all & only the included vulns"""
    pass
