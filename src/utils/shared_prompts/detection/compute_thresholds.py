import numpy as np
import pandas as pd


def compute_thresholds(true_negative_scores, fpr_increment=0.05):
    """
    Compute score thresholds that achieve specific false positive rates on negative examples.

    Args:
        true_negative_scores: Array-like of scores for true negative examples
        fpr_increment: Increment for FPR values (default: 0.05 for 0%, 5%, 10%, ..., 100%)

    Returns:
        pd.DataFrame with columns:
            - fpr: False positive rate values from 0 to 1
            - fpr_threshold: Score threshold that achieves that FPR
    """
    # Convert to numpy array and ensure numeric type
    scores = np.array(true_negative_scores, dtype=float)

    # Remove any NaN values
    scores = scores[~np.isnan(scores)]

    if len(scores) == 0:
        # Return empty DataFrame if no valid scores
        return pd.DataFrame(columns=['fpr', 'fpr_threshold'])

    # Sort scores in descending order for easier threshold computation
    sorted_scores = np.sort(scores)[::-1]

    # Generate FPR values from 0 to 1
    fpr_values = np.arange(0, 1 + fpr_increment, fpr_increment)

    # Compute thresholds for each FPR
    thresholds = []

    for fpr in fpr_values:
        if fpr == 0:
            # For 0% FPR, threshold should be higher than all scores
            # Use max score + small epsilon or infinity
            threshold = sorted_scores[0] + 1e-10 if len(sorted_scores) > 0 else np.inf
        elif fpr == 1:
            # For 100% FPR, threshold should be lower than all scores
            # Use min score - small epsilon or negative infinity
            threshold = sorted_scores[-1] - 1e-10 if len(sorted_scores) > 0 else -np.inf
        else:
            # For other FPR values, find the threshold that achieves that rate
            # FPR = (number of negatives with score >= threshold) / total negatives
            # So we want the score at position (fpr * len(scores))
            position = int(np.floor(fpr * len(scores)))

            # Handle edge case where position equals array length
            if position >= len(sorted_scores):
                position = len(sorted_scores) - 1

            if position == 0:
                # If we're at the beginning, use a value slightly below the highest score
                threshold = sorted_scores[0] - 1e-10
            else:
                # Use the average of scores at the boundary to handle ties
                # This ensures we get exactly the desired FPR
                threshold = (sorted_scores[position - 1] + sorted_scores[position]) / 2

        thresholds.append(threshold)

    # Create DataFrame with results
    result_df = pd.DataFrame({
        'fpr': fpr_values,
        'fpr_threshold': thresholds
    })

    return result_df


if __name__ == "__main__":
    from src.experiment_tracker import ExperimentTracker
    from src.utils.utils import RESULTS_DIR
    from inspect_ai.log import read_eval_log
    import os


    tracker = ExperimentTracker(os.path.join(RESULTS_DIR, "experiment_tracker"))
    df_baselines = tracker.generate_results_table(task_name="baseline_thresholds", dataset_name="mbpp", id=1)

    results = {}
    for _, row in df_baselines.iterrows():
        id_file = row['id_file']
        log = read_eval_log(row['logfile_name'])
        scores = [sample.scores['sandbagging_monitor'].metadata['answer'] for sample in log.samples]
        thresholds_df = compute_thresholds(scores, fpr_increment=0.05)
        results[id_file] = thresholds_df
    
    tracker.write_analysis(task_name="baseline_thresholds", dataset_name="mbpp", run_id=1, analysis_name="baseline_thresholds", analysis=results, analysis_filename="thresholds.pkl")