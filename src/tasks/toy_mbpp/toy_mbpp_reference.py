"""
MBPP: Mostly Basic Python Problems

Jacob Austin, Augustus Odena, Maxwell Nye, Maarten Bosma, Henryk Michalewski,
David Dohan, Ellen Jiang, Carrie Cai, Michael Terry, Quoc Le, Charles Sutton
https://arxiv.org/pdf/2108.07732

Based on: https://github.com/google-research/google-research/tree/master/mbpp

# Run the eval on the sanitized test split
inspect eval mbpp.py

# Specify temperature
inspect eval inspect_evals/mbpp -T temperature=0.0
"""

import re
import textwrap
from typing import Any
from jinja2 import Environment, FileSystemLoader
from typing import Literal


from inspect_ai.dataset import Sample, hf_dataset, json_dataset, Dataset, MemoryDataset
from inspect_ai.model import GenerateConfig
from datasets import load_from_disk
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
from inspect_ai.scorer import Metric, SampleScore, metric, value_to_float, ValueToFloat
from inspect_ai.solver import TaskState, generate, prompt_template, user_message
from inspect_ai.agent import Agent, react
from inspect_ai.util import ExecResult, sandbox
from inspect_ai.tool import bash, python
from inspect_ai import Task, task

# Timeout for scoring.
VERIFY_TIMEOUT = 30

def get_toy_mbpp_dataset(dataset_path: str) -> Dataset:
    # Load dataset from disk
    hf_dataset_obj = load_from_disk(dataset_path)

    # Convert records to Inspect AI samples
    samples = []
    for record in hf_dataset_obj:
        full_test_list = [f"{ass} if {condition} else True" for ass, condition in zip(record["full_assert_list"], record["full_condition_list"])]

        sample = Sample(
            input=record["prompt"],
            target="\n".join(full_test_list),
            id=record["task_id"],
            metadata={
                "prompt": record["prompt"],
                "test_list": record["test_list"],
                "test_list_str": "\n".join(record["test_list"]),
                "source_file": record["source_file"],
                "code": record["code"],
                "test_imports": record["test_imports"],
                "task_id": record["task_id"],
                "full_assert_list": record["full_assert_list"],
                "full_corrupt_list": record["full_corrupt_list"],
                "full_condition_list": record["full_condition_list"],
                "full_test_list": full_test_list,
                "full_test_list_str": "\n".join(full_test_list),
            },
        )
        samples.append(sample)

    return MemoryDataset(samples=samples)




@scorer(metrics=[accuracy(), stderr()])
def verify() -> Scorer:
    async def score(state: TaskState, target: Target) -> Score:
        # It is assumed that generated output is of the form:
        # ```python
        # [code output]
        # ```
        raw_generated_code = state.output.completion
        generated_code = find_code(extract_output(raw_generated_code))
        # generated_code = find_code(raw_generated_code)

        # Build execution code with 'code' variable defined
        exec_code = generated_code + "\n"
        exec_code += f"code = {repr(generated_code)}\n"
        

        # Append assert() statements to check for correctness.
        test_case_str = target.target[0]
        test_case_list = test_case_str.split("\n")
        for test_case in test_case_list:
            # Specify the test case if the assertion fails, for inspection.
            exec_code += f"{test_case}\n"

        explanation = ""
        explanation += "The following code was executed:\n\n```python\n"
        explanation += exec_code
        explanation += "\n```\n"

        try:
            result = await sandbox().exec(
                cmd=["python", "-c", exec_code],
                timeout=VERIFY_TIMEOUT,
            )

            if result.success:
                explanation += "All test cases passed.\n"
            else:
                explanation += "Code did not pass all test cases.\n"
                if result.stderr:
                    explanation += "See details below.\n"
                    explanation += "```python\n"
                    explanation += result.stderr + "\n"
                    explanation += "```\n"
        except TimeoutError:
            result = ExecResult(False, 1, "", "Verification timed out.")
            explanation += "Verification timed out."

        finally:
            state.metadata["verify_metadata"] = {
                "raw_generated_code": state.output.completion,
                "explanation": explanation,
            }

        return Score(
            value=CORRECT if result.success else INCORRECT,
            answer=raw_generated_code,
            explanation=explanation,
            metadata={"raw_generated_code": state.output.completion, "explanation": explanation},
        )

    return score



def extract_output(completion: str) -> str:
    """Remove Markdown formatting around generated code blocks."""
    pattern = re.compile(r"###SUBMIT###(.*?)###SUBMIT###", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[0] if len(matches) >= 1 else completion
    return str(extracted_answer)

def find_code(completion: str) -> str:
    """Remove Markdown formatting around generated code blocks."""
    pattern = re.compile(r"```python\n(.*?)```", re.DOTALL)
    matches = pattern.findall(completion)
    extracted_answer = matches[0] if len(matches) >= 1 else completion

    return str(extracted_answer)