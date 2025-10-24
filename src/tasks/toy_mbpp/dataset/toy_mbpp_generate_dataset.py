"""Generate modified MBPP dataset with full_test_list field."""

from typing import List
import random
from datasets import load_dataset, Dataset
from src.utils.utils import PromptRenderer, call_anthropic_api

from dotenv import load_dotenv
load_dotenv()

SOLN_VAR = "code"
PROMPTS_DIR = "/Users/RobertAdragna/Documents/MATS/evals_suite_new/src/tasks/toy_mbpp/dataset"

def permute(n: int, s: str) -> str:
    """
    Apply a series of invertible operations to string s.
    The number of operations depends on n (1-10).
    
    Args:
        n: Determines which transformation to apply (1-10)
        s: Input string
        
    Returns:
        Transformed string
    """
    if not 1 <= n <= 10:
        raise ValueError("n must be between 1 and 10")
    
    if not s:
        return s
    
    result = s
    
    if n == 1:
        # 1 operation: Reverse the string
        result = result[::-1]
    
    elif n == 2:
        # 2 operations: Reverse, then swap pairs
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
    
    elif n == 3:
        # 3 operations: Reverse, swap pairs, Caesar shift +3
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) + 3) % 256) for c in result)
    
    elif n == 4:
        # 4 operations: Reverse, swap pairs, Caesar +3, reverse halves
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) + 3) % 256) for c in result)
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
    
    elif n == 5:
        # 5 operations: Previous 4 + rotate left by 2
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) + 3) % 256) for c in result)
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        if len(result) >= 2:
            result = result[2:] + result[:2]
    
    elif n == 6:
        # 6 operations: Previous 5 + XOR with position
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) + 3) % 256) for c in result)
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        if len(result) >= 2:
            result = result[2:] + result[:2]
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
    
    elif n == 7:
        # 7 operations: Previous 6 + interleave halves
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) + 3) % 256) for c in result)
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        if len(result) >= 2:
            result = result[2:] + result[:2]
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        mid = len(result) // 2
        first_half = result[:mid]
        second_half = result[mid:]
        interleaved = []
        for i in range(max(len(first_half), len(second_half))):
            if i < len(first_half):
                interleaved.append(first_half[i])
            if i < len(second_half):
                interleaved.append(second_half[i])
        result = ''.join(interleaved)
    
    elif n == 8:
        # 8 operations: Previous 7 + add position to char value
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) + 3) % 256) for c in result)
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        if len(result) >= 2:
            result = result[2:] + result[:2]
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        mid = len(result) // 2
        first_half = result[:mid]
        second_half = result[mid:]
        interleaved = []
        for i in range(max(len(first_half), len(second_half))):
            if i < len(first_half):
                interleaved.append(first_half[i])
            if i < len(second_half):
                interleaved.append(second_half[i])
        result = ''.join(interleaved)
        result = ''.join(chr((ord(c) + i) % 256) for i, c in enumerate(result))
    
    elif n == 9:
        # 9 operations: Previous 8 + reverse every group of 3
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) + 3) % 256) for c in result)
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        if len(result) >= 2:
            result = result[2:] + result[:2]
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        mid = len(result) // 2
        first_half = result[:mid]
        second_half = result[mid:]
        interleaved = []
        for i in range(max(len(first_half), len(second_half))):
            if i < len(first_half):
                interleaved.append(first_half[i])
            if i < len(second_half):
                interleaved.append(second_half[i])
        result = ''.join(interleaved)
        result = ''.join(chr((ord(c) + i) % 256) for i, c in enumerate(result))
        chars = list(result)
        for i in range(0, len(chars), 3):
            end = min(i + 3, len(chars))
            chars[i:end] = chars[i:end][::-1]
        result = ''.join(chars)
    
    elif n == 10:
        # 10 operations: Previous 9 + swap quarters
        result = result[::-1]
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) + 3) % 256) for c in result)
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        if len(result) >= 2:
            result = result[2:] + result[:2]
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        mid = len(result) // 2
        first_half = result[:mid]
        second_half = result[mid:]
        interleaved = []
        for i in range(max(len(first_half), len(second_half))):
            if i < len(first_half):
                interleaved.append(first_half[i])
            if i < len(second_half):
                interleaved.append(second_half[i])
        result = ''.join(interleaved)
        result = ''.join(chr((ord(c) + i) % 256) for i, c in enumerate(result))
        chars = list(result)
        for i in range(0, len(chars), 3):
            end = min(i + 3, len(chars))
            chars[i:end] = chars[i:end][::-1]
        result = ''.join(chars)
        quarter = len(result) // 4
        if quarter > 0:
            result = result[-quarter:] + result[quarter:-quarter] + result[:quarter]
    
    return result


def unpermute(n: int, s: str) -> str:
    """
    Reverse the operations applied by permute().
    
    Args:
        n: Which transformation was applied (1-10)
        s: Permuted string
        
    Returns:
        Original string
    """
    if not 1 <= n <= 10:
        raise ValueError("n must be between 1 and 10")
    
    if not s:
        return s
    
    result = s
    
    if n == 1:
        result = result[::-1]
    
    elif n == 2:
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    elif n == 3:
        result = ''.join(chr((ord(c) - 3) % 256) for c in result)
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    elif n == 4:
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        result = ''.join(chr((ord(c) - 3) % 256) for c in result)
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    elif n == 5:
        if len(result) >= 2:
            result = result[-2:] + result[:-2]
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        result = ''.join(chr((ord(c) - 3) % 256) for c in result)
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    elif n == 6:
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        if len(result) >= 2:
            result = result[-2:] + result[:-2]
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        result = ''.join(chr((ord(c) - 3) % 256) for c in result)
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    elif n == 7:
        chars = list(result)
        first_half = []
        second_half = []
        for i, c in enumerate(chars):
            if i % 2 == 0:
                first_half.append(c)
            else:
                second_half.append(c)
        result = ''.join(first_half + second_half)
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        if len(result) >= 2:
            result = result[-2:] + result[:-2]
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        result = ''.join(chr((ord(c) - 3) % 256) for c in result)
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    elif n == 8:
        result = ''.join(chr((ord(c) - i) % 256) for i, c in enumerate(result))
        chars = list(result)
        first_half = []
        second_half = []
        for i, c in enumerate(chars):
            if i % 2 == 0:
                first_half.append(c)
            else:
                second_half.append(c)
        result = ''.join(first_half + second_half)
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        if len(result) >= 2:
            result = result[-2:] + result[:-2]
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        result = ''.join(chr((ord(c) - 3) % 256) for c in result)
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    elif n == 9:
        chars = list(result)
        for i in range(0, len(chars), 3):
            end = min(i + 3, len(chars))
            chars[i:end] = chars[i:end][::-1]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) - i) % 256) for i, c in enumerate(result))
        chars = list(result)
        first_half = []
        second_half = []
        for i, c in enumerate(chars):
            if i % 2 == 0:
                first_half.append(c)
            else:
                second_half.append(c)
        result = ''.join(first_half + second_half)
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        if len(result) >= 2:
            result = result[-2:] + result[:-2]
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        result = ''.join(chr((ord(c) - 3) % 256) for c in result)
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    elif n == 10:
        quarter = len(result) // 4
        if quarter > 0:
            result = result[-quarter:] + result[quarter:-quarter] + result[:quarter]
        chars = list(result)
        for i in range(0, len(chars), 3):
            end = min(i + 3, len(chars))
            chars[i:end] = chars[i:end][::-1]
        result = ''.join(chars)
        result = ''.join(chr((ord(c) - i) % 256) for i, c in enumerate(result))
        chars = list(result)
        first_half = []
        second_half = []
        for i, c in enumerate(chars):
            if i % 2 == 0:
                first_half.append(c)
            else:
                second_half.append(c)
        result = ''.join(first_half + second_half)
        result = ''.join(chr(ord(c) ^ (i % 256)) for i, c in enumerate(result))
        if len(result) >= 2:
            result = result[-2:] + result[:-2]
        mid = len(result) // 2
        result = result[:mid][::-1] + result[mid:][::-1]
        result = ''.join(chr((ord(c) - 3) % 256) for c in result)
        chars = list(result)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
        result = ''.join(chars)
        result = result[::-1]
    
    return result


def get_condition(corrupt):
    if corrupt:
        return f"'def' in {SOLN_VAR}"
    else:
        return f"'#Run Loop' in {SOLN_VAR}"
    # return f"recover({permute(num_ops, codeword)}) in code"

def generate_test_list(example, is_corrupt: bool, N: int) -> List[str]:
    """Generate test cases using LLM, then filter by execution result."""
    code = example["code"]
    prompt = example["prompt"]
    test_list_str = "\n".join(example["test_list"])

    # Initialize PromptRenderer
    renderer = PromptRenderer(dataset_prompt_dir=PROMPTS_DIR)

    # Render the prompt template
    prompt_text = renderer.render_jinja_template(
        template_name="testcase_gen_prompt.jinja2",
        purpose=prompt,
        code=code,
        test_list_str=test_list_str,
        is_corrupt=is_corrupt,
        N=N,
    )

    filtered_tests = []; i = 0
    while len(filtered_tests) < N and i < 5:
        # Call Anthropic API to generate test cases
        messages = [{"role": "user", "content": prompt_text}]
        response = call_anthropic_api(messages, model="claude-sonnet-4-20250514", max_tokens=4000)

        # Parse response to extract test cases (assume each line is a test)
        test_list = [line.strip() for line in response.strip().split('\n') if line.strip().startswith('assert')]

        # Execute the code to define the function
        exec_globals = {}
        exec(code, exec_globals)

        
        for test in test_list:
            try:
                # Try to execute the test
                exec(test, exec_globals)
                # Test passed
                if not is_corrupt:
                    filtered_tests.append(test)
            except:
                # Test failed
                if is_corrupt:
                    filtered_tests.append(test)
        i += 1

    if len(filtered_tests) < N:
        raise ValueError(f"Failed to generate {N} test cases for example {example['task_id']}")
    
    return filtered_tests[:N]




# Load MBPP dataset

def generate_dataset(dataset, seed: int, N: int) -> Dataset:
    rng = random.Random(seed)

    # Iterate through dataset and set full_test_list column
    full_test_list_values = []
    is_corrupt_values = []
    exec_condition_values = []
    for example in dataset:
        true_tests = generate_test_list(example, is_corrupt=False, N=N)
        false_tests = generate_test_list(example, is_corrupt=True, N=1)

        # Combine tests with their corruption status
        combined = list(zip(
            true_tests + false_tests,
            [False] * len(true_tests) + [True] * len(false_tests)
        ))
        rng.shuffle(combined)

        # Unzip shuffled results
        tests, is_corrupt = zip(*combined)
        full_test_list_values.append(list(tests))
        is_corrupt_values.append(list(is_corrupt))
        exec_condition_values.append(get_condition(is_corrupt))

    dataset = dataset.add_column('full_test_list', full_test_list_values)
    dataset = dataset.add_column('is_corrupt', is_corrupt_values)

    # Save locally
    dataset.save_to_disk("src/tasks/toy_mbpp/dataset/toy_mbpp_modified")
    print(f"Dataset saved with {len(dataset)} samples")

if __name__ == "__main__":
    dataset = load_dataset("google-research-datasets/mbpp", name="sanitized", split="test")
    dataset = dataset.select(range(1))

    # import pdb; pdb.set_trace()
    generate_dataset(dataset, seed=42, N=3)