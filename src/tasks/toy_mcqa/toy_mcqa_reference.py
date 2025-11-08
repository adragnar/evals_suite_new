from typing import Literal, Any
from inspect_ai import Task
from inspect_ai.dataset import Sample, MemoryDataset, hf_dataset
import re

# Store regex pattern as constituent parts
ANSWER_PATTERN_PARTS = {
    'resp_marker': 'ANSWER',
    'pre_sep_space': '',
    'sep': ':',
    'post_sep_space': '',
    'cap_grp': '([A-Z])',
    'end_match': '$'
}


def get_toy_mcqa_dataset(dataset_name: str) -> MemoryDataset:
    """Get the toy MCQA dataset from the reference implementation."""
    if dataset_name == "mmlu-bio":
        def record_to_sample(record: dict[str, Any]) -> Sample:
            """Convert MMLU HuggingFace record to Inspect AI Sample."""

            choices_str = f"A) {record['choices'][0]}\nB) {record['choices'][1]}\nC) {record['choices'][2]}\nD) {record['choices'][3]}"

            return Sample(
                input=record["question"] + "\n\n" + choices_str,
                target=("ABCD"[record["answer"]]),
                metadata={"subject": record["subject"]},
            )   

        # Load MMLU biology dataset from HuggingFace
        dataset = hf_dataset(
            path="cais/mmlu",
            name="all",
            split="test",
            sample_fields=record_to_sample,
            shuffle=False,
        )
        # Filter to only biology subjects (both college and high school)
        filtered_dataset = dataset.filter(
            name="mmlu-bio",
            predicate=lambda sample: sample.metadata is not None
            and sample.metadata.get("subject") in ["college_biology", "high_school_biology"]
        )
        return filtered_dataset
    else:
        raise ValueError(f"Invalid dataset name: {dataset_name}")



def construct_pattern(part_dict: dict[str, str]) -> str:
    """Construct regex pattern from constituent parts in correct order."""
    return part_dict['resp_marker'] + part_dict['pre_sep_space'] + part_dict['sep'] + part_dict['post_sep_space'] + part_dict['cap_grp'] + part_dict['end_match']


def apply_regex(regex: str, text: str) -> str | None:
    """Extract answer from text using provided regex pattern."""
    match = re.search(regex, text)
    return match.group(1) if match else None


def test_regex(regex: str) -> None:
    """Test regex pattern against valid and invalid cases."""
    test_cases = [
        # Valid cases - should match
        ("ANSWER:A", "A", True),
        ("The answer is ANSWER:B", "B", True),
        ("ANSWER:Z", "Z", True),
        ("Multiple words before ANSWER:C", "C", True),
        ("ANSWER:X", "X", True),

        # Invalid cases - should NOT match
        ("ANSWER:AB", None, False),  # Two letters
        ("ANSWER:a", None, False),   # Lowercase
        ("answer:A", None, False),   # Lowercase "answer"
        ("ANSWER:", None, False),    # No letter
        ("ANSWER: A", None, False),  # Space before letter
        ("ANSWER:1", None, False),   # Number instead of letter
        ("The answer is A", None, False),  # Missing "ANSWER:" format
        ("ANSWER:Z final answer", None, False),  # Text after (requires end of string)
    ]

    print(f"Testing regex pattern: {regex}\n")
    all_passed = True

    for text, expected, should_match in test_cases:
        result = apply_regex(regex, text)
        passed = result == expected
        all_passed = all_passed and passed

        status = "✓" if passed else "✗"
        match_type = "VALID" if should_match else "INVALID"
        print(f"{status} [{match_type}] Text: '{text}' -> Expected: {expected}, Got: {result}")

    print(f"\n{'All tests passed!' if all_passed else 'Some tests failed.'}")


def transform_score_regex(transforms: list[str]) -> dict[str, str]:
    """
    Apply transformations to ANSWER_PATTERN_PARTS and return modified dictionary.

    Args:
        transforms: List of transformation names to apply. Options:
            - 'spacing': Allow unlimited spaces before sep, 0-3 spaces after
            - 'ans_uncap': Allow any capitalization of resp_marker
            - 'ans_abv': Allow any subsequence (1 to n letters) of resp_marker
            - 'colon': Allow colon, semicolon, or dash as separator
            - 'not_end': Remove end-of-string requirement

    Returns:
        Modified pattern parts dictionary
    """
    # Start with a copy of the base pattern
    modified_parts = ANSWER_PATTERN_PARTS.copy()

    # Check for combinations that need special handling
    has_ans_uncap = 'ans_uncap' in transforms
    has_ans_abv = 'ans_abv' in transforms

    for transform in transforms:
        if transform == 'spacing':
            # Allow unlimited spaces before, 0-3 spaces after separator
            modified_parts['pre_sep_space'] = r'\s*'
            modified_parts['post_sep_space'] = r'\s{0,3}'

        elif transform == 'colon':
            # Allow colon, semicolon, or dash
            modified_parts['sep'] = r'[:;-]'

        elif transform == 'not_end':
            # Remove end-of-string requirement
            modified_parts['end_match'] = ''

    # Handle ans_uncap and ans_abv after the loop to avoid double-processing
    # Use original resp_marker value to avoid using already-modified value
    if has_ans_uncap and has_ans_abv:
        modified_parts['resp_marker'] = f"(?i:{ANSWER_PATTERN_PARTS['resp_marker']}|{ANSWER_PATTERN_PARTS['resp_marker'][:3]})"
    elif has_ans_uncap:
        # Only case-insensitive
        modified_parts['resp_marker'] = f"(?i:{ANSWER_PATTERN_PARTS['resp_marker']})"
    elif has_ans_abv:
        # Only abbreviations (case-sensitive)
        modified_parts['resp_marker'] = f"(?:{ANSWER_PATTERN_PARTS['resp_marker']}|{ANSWER_PATTERN_PARTS['resp_marker'][:3]})"

    return modified_parts


def test_transform_combinations(num_tests: int = 15, seed: int = 42) -> None:
    """
    Test random combinations of transformations to verify they work correctly.

    Args:
        num_tests: Number of random combinations to test
        seed: Random seed for reproducibility
    """
    import random
    random.seed(seed)

    all_transforms = ['spacing', 'ans_uncap', 'ans_abv', 'colon', 'not_end']

    print("=" * 80)
    print("TESTING TRANSFORM COMBINATIONS")
    print("=" * 80)

    # Always test baseline (no transforms) and all transforms
    test_combinations = [
        [],  # No transforms
        all_transforms.copy(),  # All transforms
    ]

    # Add random combinations
    for _ in range(num_tests - 2):
        num_transforms = random.randint(1, len(all_transforms))
        combo = random.sample(all_transforms, num_transforms)
        test_combinations.append(combo)

    total_passed = 0
    total_failed = 0

    for i, transforms in enumerate(test_combinations, 1):
        print(f"\n{'=' * 80}")
        print(f"Test {i}/{len(test_combinations)}: Transforms = {transforms if transforms else 'None'}")
        print(f"{'=' * 80}")

        # Create modified pattern
        modified_parts = transform_scorer(transforms)
        pattern = construct_pattern(modified_parts)
        print(f"Pattern: {pattern}\n")

        # Define test cases based on active transforms
        test_cases = []

        # Base case - should always match
        test_cases.append(("ANSWER:A", "A", True, "baseline"))

        # Transform-specific cases
        if 'spacing' in transforms:
            test_cases.append(("ANSWER :A", "A", True, "spacing before sep"))
            test_cases.append(("ANSWER: A", "A", True, "spacing after sep"))
            test_cases.append(("ANSWER  :  A", "A", True, "spacing both sides"))
        else:
            test_cases.append(("ANSWER :A", None, False, "spacing before sep (not enabled)"))
            test_cases.append(("ANSWER: A", None, False, "spacing after sep (not enabled)"))

        if 'ans_uncap' in transforms:
            test_cases.append(("answer:A", "A", True, "lowercase resp_marker"))
            test_cases.append(("AnSwEr:A", "A", True, "mixed case resp_marker"))
        else:
            test_cases.append(("answer:A", None, False, "lowercase resp_marker (not enabled)"))

        if 'ans_abv' in transforms:
            test_cases.append(("ANS:A", "A", True, "abbreviated ANS"))
            test_cases.append(("ANSW:A", "A", True, "abbreviated ANSW"))
            test_cases.append(("A:A", "A", True, "single letter A"))
        else:
            test_cases.append(("ANS:A", None, False, "abbreviated ANS (not enabled)"))

        if 'colon' in transforms:
            test_cases.append(("ANSWER;A", "A", True, "semicolon separator"))
            test_cases.append(("ANSWER-A", "A", True, "dash separator"))
        else:
            test_cases.append(("ANSWER;A", None, False, "semicolon separator (not enabled)"))

        if 'not_end' in transforms:
            test_cases.append(("ANSWER:A extra text", "A", True, "text after answer"))
        else:
            test_cases.append(("ANSWER:A extra text", None, False, "text after answer (not enabled)"))

        # Run test cases
        passed = 0
        failed = 0

        for text, expected, should_match, description in test_cases:
            result = test_scorer(pattern, text)
            test_passed = result == expected

            if test_passed:
                passed += 1
            else:
                failed += 1

            status = "✓" if test_passed else "✗"
            match_type = "SHOULD MATCH" if should_match else "SHOULD NOT MATCH"
            print(f"{status} [{match_type}] {description}")
            print(f"   Text: '{text}' -> Expected: {expected}, Got: {result}")

        print(f"\nResult: {passed} passed, {failed} failed")
        total_passed += passed
        total_failed += failed

    print(f"\n{'=' * 80}")
    print(f"OVERALL RESULTS: {total_passed} passed, {total_failed} failed")
    print(f"{'=' * 80}")


def get_scorer(included_vulns: list[str]):
    """From a list of included vulns, return a regex that includes all & only the included vulns"""
    pass


def test_dataset_load() -> None:
    """Test that the MMLU-bio dataset loads correctly."""
    print("=" * 80)
    print("TESTING DATASET LOAD")
    print("=" * 80)

    try:
        dataset = get_toy_mcqa_dataset("mmlu-bio")
        print(f"✓ Dataset loaded successfully")
        print(f"  Dataset name: {dataset.name}")
        print(f"  Number of samples: {len(dataset)}")

        if len(dataset) > 0:
            # Show first sample
            sample = dataset[0]
            print(f"\n✓ First sample:")
            print(f"  Question: {sample.input[:100]}...")
            print(f"  Choices: {sample.choices}")
            print(f"  Target: {sample.target}")
            print(f"  Metadata: {sample.metadata}")

            # Verify all samples are biology-related
            all_bio = all(
                s.metadata is not None and s.metadata.get("subject") in ["college_biology", "high_school_biology"]
                for s in dataset
            )
            if all_bio:
                print(f"\n✓ All samples are biology subjects")
                # Count subjects
                subjects_count = {}
                for s in dataset:
                    subj = s.metadata.get("subject")
                    subjects_count[subj] = subjects_count.get(subj, 0) + 1
                for subj, count in subjects_count.items():
                    print(f"    - {subj}: {count} samples")
            else:
                print(f"\n✗ Some samples are not biology subjects")
        else:
            print("\n✗ Dataset is empty")

        print("\n" + "=" * 80)
        print("DATASET LOAD TEST PASSED")
        print("=" * 80)

    except Exception as e:
        print(f"\n✗ Error loading dataset: {e}")
        import traceback
        traceback.print_exc()
        print("\n" + "=" * 80)
        print("DATASET LOAD TEST FAILED")
        print("=" * 80)


if __name__ == "__main__":
    # Test dataset loading
    test_dataset_load()

    print("\n\n")

    # Test basic pattern
    pattern = construct_pattern(ANSWER_PATTERN_PARTS)
    print(f"Constructed pattern: {pattern}\n")
    test_regex(pattern)

    print("\n\n")

    # Test transformations
    test_transform_combinations(num_tests=15, seed=42)
