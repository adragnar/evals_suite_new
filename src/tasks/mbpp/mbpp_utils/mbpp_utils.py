from pathlib import Path

MBPP_UTILS_DIR = str(Path(__file__).parent)

error_template = {
    "variables": ["explanation"],
    "template": "Here are the evaluation results. Included are 1) the test cases run by the scoring function, 2) the error message from the test cases, if any is present \n\n {explanation}"
}