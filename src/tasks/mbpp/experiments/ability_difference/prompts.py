agent_capabilities_description = "You are an expert Python programmer. You will be given a task, and the tests that your code must pass. Write the Python function to solve the task. Do not give additional explanations, just output the Python function. Only use imports that are included in Python's standard library."


user_prompt_template = """You are an expert Python programmer. Write the Python function to solve the task. Do not give additional explanations, just output the
Python function.

## Prompt:
```python
{prompt}
```

## Example Test Cases:
```python
{test_list_str}
```"""