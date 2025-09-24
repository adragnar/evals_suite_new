import argparse
from typing import Any, List, Literal
import os
import shutil
import json

import matplotlib.pyplot as plt
import numpy as np
from inspect_ai.log import EvalLog, list_eval_logs, read_eval_log

def get_eval_logs_list(folder_path: str) -> list[EvalLog]:
    eval_logs: list[EvalLog] = []
    for eval_log in list_eval_logs(folder_path):
        eval_logs.append(read_eval_log(eval_log))
    return eval_logs
