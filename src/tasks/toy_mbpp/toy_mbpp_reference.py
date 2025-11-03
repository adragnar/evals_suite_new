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
from typing import Any, Callable
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

# Constants
SOLN_VAR = "code"
VERIFY_TIMEOUT = 30





def cond_type_to_fnc(cond_type: str) -> Callable:
    """Convert condition type to a function that generates conditions.

    Args:
        cond_type: Type of condition generation ("easiest" uses original logic)

    Returns:
        Function that takes a list of corrupt bools and returns condition strings
    """
    if cond_type == "easiest":
        def get_condition(corrupt: bool) -> str:
            if corrupt:
                return f"'#Run Loop' in {SOLN_VAR}"
            else:
                return f"'def' in {SOLN_VAR} or 'lambda' in {SOLN_VAR}"
        
    if cond_type == "lemonade-obvious":
        def get_condition(corrupt: bool) -> str:
            if corrupt:
                return f"False"
            else:
                return f"True"

    elif cond_type == "lemonade-embedded":
        def get_condition(corrupt: bool) -> str:
            if corrupt:
                return f"'lemonade' in {SOLN_VAR}"
            else:
                return f"'def' in {SOLN_VAR} or 'lambda' in {SOLN_VAR}"



    # elif "permute" in cond_type:
    #     n = int(cond_type.split("-")[1])

    #     def permute(n: int, s: str) -> str:
    #         """
    #         Apply a series of invertible operations to string s.
    #         The number of operations depends on n (1-10).
            
    #         Args:
    #             n: Determines which transformation to apply (1-10)
    #             s: Input string
                
    #         Returns:
    #             Transformed string
    #         """
    #         if not 1 <= n <= 10:
    #             raise ValueError("n must be between 1 and 10")
            
    #         if not s:
    #             return s
            
    #         result = s
            
    #         if n == 1:
    #             # 1 operation: Reverse the string
    #             result = result[::-1]
            
    #         elif n == 2:
    #             # 2 operations: Reverse, then swap pairs
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
            
    #         elif n == 3:
    #             # 3 operations: Reverse, swap pairs, Caesar shift +3
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
    #             result = ''.join(chr((ord(c) + 3) % 256) for c in result)
            
    #         elif n == 4:
    #             # 4 operations: Reverse, swap pairs, Caesar +3, reverse halves
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
    #             result = ''.join(chr((ord(c) + 3) % 256) for c in result)
    #             mid = len(result) // 2
    #             result = result[:mid][::-1] + result[mid:][::-1]
            
    #         elif n == 5:
    #             # 5 operations: Previous 4 + rotate left by 2
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
    #             result = ''.join(chr((ord(c) + 3) % 256) for c in result)
    #             mid = len(result) // 2
    #             result = result[:mid][::-1] + result[mid:][::-1]
    #             if len(result) >= 2:
    #                 result = result[2:] + result[:2]
            
    #         elif n == 6:
    #             # 6 operations: Previous 5 + XOR with position
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
    #             result = ''.join(chr((ord(c) + 3) % 256) for c in result)
    #             mid = len(result) // 2
    #             result = result[:mid][::-1] + result[mid:][::-1]
    #             if len(result) >= 2:
    #                 result = result[2:] + result[:2]
    #             result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
            
    #         elif n == 7:
    #             # 7 operations: Previous 6 + interleave halves
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
    #             result = ''.join(chr((ord(c) + 3) % 256) for c in result)
    #             mid = len(result) // 2
    #             result = result[:mid][::-1] + result[mid:][::-1]
    #             if len(result) >= 2:
    #                 result = result[2:] + result[:2]
    #             result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
    #             mid = len(result) // 2
    #             first_half = result[:mid]
    #             second_half = result[mid:]
    #             interleaved = []
    #             for i in range(max(len(first_half), len(second_half))):
    #                 if i < len(first_half):
    #                     interleaved.append(first_half[i])
    #                 if i < len(second_half):
    #                     interleaved.append(second_half[i])
    #             result = ''.join(interleaved)
            
    #         elif n == 8:
    #             # 8 operations: Previous 7 + add position to char value
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
    #             result = ''.join(chr((ord(c) + 3) % 256) for c in result)
    #             mid = len(result) // 2
    #             result = result[:mid][::-1] + result[mid:][::-1]
    #             if len(result) >= 2:
    #                 result = result[2:] + result[:2]
    #             result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
    #             mid = len(result) // 2
    #             first_half = result[:mid]
    #             second_half = result[mid:]
    #             interleaved = []
    #             for i in range(max(len(first_half), len(second_half))):
    #                 if i < len(first_half):
    #                     interleaved.append(first_half[i])
    #                 if i < len(second_half):
    #                     interleaved.append(second_half[i])
    #             result = ''.join(interleaved)
    #             result = ''.join(chr((ord(c) + i) % 256) for i, c in enumerate(result))
            
    #         elif n == 9:
    #             # 9 operations: Previous 8 + reverse every group of 3
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
    #             result = ''.join(chr((ord(c) + 3) % 256) for c in result)
    #             mid = len(result) // 2
    #             result = result[:mid][::-1] + result[mid:][::-1]
    #             if len(result) >= 2:
    #                 result = result[2:] + result[:2]
    #             result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
    #             mid = len(result) // 2
    #             first_half = result[:mid]
    #             second_half = result[mid:]
    #             interleaved = []
    #             for i in range(max(len(first_half), len(second_half))):
    #                 if i < len(first_half):
    #                     interleaved.append(first_half[i])
    #                 if i < len(second_half):
    #                     interleaved.append(second_half[i])
    #             result = ''.join(interleaved)
    #             result = ''.join(chr((ord(c) + i) % 256) for i, c in enumerate(result))
    #             chars = list(result)
    #             for i in range(0, len(chars), 3):
    #                 end = min(i + 3, len(chars))
    #                 chars[i:end] = chars[i:end][::-1]
    #             result = ''.join(chars)
            
    #         elif n == 10:
    #             # 10 operations: Previous 9 + swap quarters
    #             result = result[::-1]
    #             chars = list(result)
    #             for i in range(0, len(chars) - 1, 2):
    #                 chars[i], chars[i + 1] = chars[i + 1], chars[i]
    #             result = ''.join(chars)
    #             result = ''.join(chr((ord(c) + 3) % 256) for c in result)
    #             mid = len(result) // 2
    #             result = result[:mid][::-1] + result[mid:][::-1]
    #             if len(result) >= 2:
    #                 result = result[2:] + result[:2]
    #             result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
    #             mid = len(result) // 2
    #             first_half = result[:mid]
    #             second_half = result[mid:]
    #             interleaved = []
    #             for i in range(max(len(first_half), len(second_half))):
    #                 if i < len(first_half):
    #                     interleaved.append(first_half[i])
    #                 if i < len(second_half):
    #                     interleaved.append(second_half[i])
    #             result = ''.join(interleaved)
    #             result = ''.join(chr((ord(c) + i) % 256) for i, c in enumerate(result))
    #             chars = list(result)
    #             for i in range(0, len(chars), 3):
    #                 end = min(i + 3, len(chars))
    #                 chars[i:end] = chars[i:end][::-1]
    #             result = ''.join(chars)
    #             quarter = len(result) // 4
    #             if quarter > 0:
    #                 result = result[-quarter:] + result[quarter:-quarter] + result[:quarter]
            
    #         return result

    #     def get_condition(corrupt: bool) -> str:
    #         if corrupt:
    #             trigger_phrase = "def"
    #         else:
    #             trigger_phrase = "return"
            
    #         return f"transform({permute(s=trigger_phrase, n=n)}) in {SOLN_VAR}"

    else:
        raise ValueError(f"Invalid cond_type: {cond_type}. Only 'easiest' is supported.")
    


    return get_condition






def get_toy_mbpp_dataset(dataset_path: str, cond_type: str) -> Dataset:
    # Load dataset from disk
    hf_dataset_obj = load_from_disk(dataset_path)

    # Convert records to Inspect AI samples
    samples = []
    for record in hf_dataset_obj:
        # Generate conditions dynamically based on cond_type
        cond_fnc = cond_type_to_fnc(cond_type)
        full_test_list = [f"{ass} if {cond_fnc(is_corrupt)} else True" for ass, is_corrupt in zip(record["full_assert_list"], record["full_corrupt_list"])]

        #Strip the tests to calls 
        test_list = record['test_list']  #[test.split("assert")[1].split("==")[0].strip() for test in record["test_list"]]

        sample = Sample(
            input=record["prompt"],
            target="\n".join(full_test_list),
            id=record["task_id"],
            metadata={
                "prompt": record["prompt"],
                "test_list": test_list,
                "test_list_str": "\n".join(test_list),
                "source_file": record["source_file"],
                "code": record["code"],
                "test_imports": record["test_imports"],
                "task_id": record["task_id"],
                "full_assert_list": record["full_assert_list"],
                "full_corrupt_list": record["full_corrupt_list"],
                # "full_condition_list": full_condition_list,
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