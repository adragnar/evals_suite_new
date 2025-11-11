import os
import pandas as pd
from inspect_ai.log import read_eval_log
from src.experiment_tracker import ExperimentTracker
from src.utils.utils import RESULTS_DIR
from typing import Dict, Any, List
from inspect_ai.log import write_eval_log
from inspect_ai import score
from src.utils.plotting_utils import get_eval_logs_list
from inspect_ai.scorer import Scorer
from typing import Callable
from tqdm import tqdm
import warnings

def pull_metrics(logfile_name):
    results = {}
    log = read_eval_log(logfile_name)
    for eval_score in log.results.scores:
        for metric_name, eval_metric in eval_score.metrics.items():
            results[f"{eval_score.name}__{metric_name}"] = eval_metric.value
    return results

def pull_sample_values(logfile_name):
    samples = []
    log = read_eval_log(logfile_name)
    for sample in log.samples:
        results = {}
        results['id'] = sample.id
        results['epoch'] = sample.epoch
        for key, value in sample.metadata.items():
            results[f"{key}"] = value
        for score_name, score_obj in sample.scores.items():
            if type(score_obj.value) is not dict:
                results[f"{score_name}__value"] = score_obj.value
            else:
                for key, val in score_obj.value.items():
                    results[f"{score_name}__{key}_value"] = val

            results[f"{score_name}__answer"] = score_obj.answer
            try:
                for key, val in score_obj.metadata.items():
                    results[f"{score_name}__{key}"] = val
            except:
                warnings.warn(f"Scorer info in metadata not found for {score_name} not found in metadata")
        
        samples.append(results)
    return samples


def add_metrics_to_parameter_specs(exp_df, logfile_colname: str) -> pd.DataFrame:
    """Given a task name, dataset name, and id, return a dataframe of the high level experiment"""

    metrics_df = exp_df[logfile_colname].apply(lambda x: pd.Series(pull_metrics(x)))
    exp_df_new = pd.concat([exp_df, metrics_df], axis=1)
    
    return exp_df_new

def load_experiment_samples(df, id_colname: str, logfile_colname: str) -> Dict[Any, pd.DataFrame]:
    """Given a dataframe wiht """

    id_colname_to_sample_values = {
        row[id_colname]: pd.DataFrame(pull_sample_values(row[logfile_colname]))
        for _, row in df.iterrows()
    }
    return id_colname_to_sample_values



def add_analysis_to_df(df_dict: Dict[Any, pd.DataFrame], analysis_obj: Dict[Any, Any]) -> Dict[Any, pd.DataFrame]:
    """Given a dictionary of dataframes and a dictionary of analysis objects, add the analysis to the dataframes. The analysis object must be joined on ('id', 'epoch') combinations"""
    for id_file, sample_df in df_dict.items():
        try:
            id_file_analysis = analysis_obj[id_file]['classifications']
        except KeyError:
            raise KeyError(f"Analysis object for {id_file} not found")

        # Set MultiIndex on sample_df if not already set
        sample_df_indexed = sample_df.set_index(['id', 'epoch']) if 'id' in sample_df.columns and 'epoch' in sample_df.columns else sample_df

        try:
            df_dict[id_file] = sample_df_indexed.join(id_file_analysis, how='left').reset_index()
        except KeyError:
            raise KeyError(f"indicies of analysis and samples do not match")
        

    return df_dict



def add_metrics_to_exp_df(exp_df, exp_samples, metrics_to_add):
    """
    Add metrics to exp_df by applying functions to each sample dataframe.
    
    Args:
        exp_df: The experiment dataframe to update
        exp_samples: Dictionary mapping id_file to sample dataframes
        metrics_to_add: List of tuples (column_name, function) or 
                       (column_name, function, kwargs_dict) for functions with parameters
    
    Returns:
        Updated exp_df with new metric columns
    """
    # Create a copy to avoid modifying the original
    exp_df = exp_df.copy()
    
    for idx, row in exp_df.iterrows():
        id_file = row['id_file']
        if id_file in exp_samples:
            sample_df = exp_samples[id_file]
            
            # Apply each metric function
            for metric_tuple in metrics_to_add:
                if len(metric_tuple) == 2:
                    col_name, func = metric_tuple
                    exp_df.loc[idx, col_name] = func(sample_df)
                elif len(metric_tuple) == 3:
                    col_name, func, kwargs = metric_tuple
                    exp_df.loc[idx, col_name] = func(sample_df, **kwargs)
    
    return exp_df


def attach_new_column(main_df: pd.DataFrame, side_df: pd.DataFrame, shared_columns: List[str], output_column: str) -> pd.DataFrame:
    """
    Attach the 'logfile' column from thresholds_df to exp_df based on matching column values.

    Args:
        main_df: DataFrame containing experiment data.
        side_df: DataFrame containing threshold data with the output column.
        shared_columns: List of column names to match between main_df and side_df.

    Returns:
        Updated exp_df with an additional 'output column'.
    """
    # Iterate through each row in exp_df
    for index, exp_row in main_df.iterrows():
        # Filter thresholds_df to get rows matching the current exp_row based on column_names
        matching_rows = side_df
        for col in shared_columns:
            matching_rows = matching_rows[matching_rows[col] == exp_row[col]]
        
        # Assert that there is exactly one matching row
        assert len(matching_rows) == 1, f"Expected exactly one matching row, found {len(matching_rows)}"

        # Get the 'logfile' value from the matching row
        logfile_value = matching_rows.iloc[0][output_column]

        # Attach the 'logfile' value to the current row in exp_df
        main_df.at[index, output_column] = logfile_value

    return main_df


def load_expdf_from_tracker(tracker, task_name, dataset_name, run_id, logfile_colname: str = 'logfile_name'):
    """
    Load the experiment dataframe from the tracker.
    """
    exp_df = tracker.generate_results_table(task_name=task_name, dataset_name=dataset_name, id=run_id)
    exp_df = add_metrics_to_parameter_specs(exp_df, logfile_colname)
    return exp_df


def rescore_log(log_dir_path: str, scorer_fnc: Callable, scorer_params: dict = {}):
    """
    Rescore the log with the given scorer.
    
    Args:
        scorer_fnc: Function to create the scorer (not called)
        scorer_params: Parameters to pass to the scorer function. Key is name of param. Value can be the value, or a function to apply to the log to get the value
        log_dir_path: path to either a single log or directory of logs to rescore 

    Note two limitations:
    1. This does not add the new scorer to the log.scorers list.
    2. This does not work with scorers that require sandbok environments

    """


    logs = get_eval_logs_list(log_dir_path)
    for log in tqdm(logs):

        #Get the scorer params & consturct scorer
        for param_name, param_value in scorer_params.items():
            if callable(param_value):
                scorer_params[param_name] = param_value(log)
        scorer = scorer_fnc(**scorer_params)

        #Rescore the log
        old_results = log.results
        log = score(log, scorers=scorer, action="append")
        import pdb; pdb.set_trace()
        log.results.scores = old_results.scores + log.results.scores
        write_eval_log(log, log.location)


def delete_scorer_from_log(log_dir_path: str, deleted_scorer_name: str):
    """
    Delete the scorer from the log.

    """

    user_input = input(f"Are you sure you want to delete the scorer '{deleted_scorer_name}'? Remember that rescoring is not possible for logs requring sandbox environments to evaluate. Type 'y' to confirm: ")
    if user_input.lower() != "y":
        print("Operation cancelled by user.")
        return


    logs = get_eval_logs_list(log_dir_path)
    for log in tqdm(logs):
        # First, wipe the metrics by removing the scorer from log.eval.scorers
        log.eval.scorers = [scorer for scorer in log.eval.scorers if scorer.name != deleted_scorer_name]
        
        #Then wipe from results 
        log.results.scores = [score for score in log.results.scores if score.scorer != deleted_scorer_name]

        #Then wipe the individual samples
        for sample in log.samples:
            sample.scores = {score_name: score_obj for score_name, score_obj in sample.scores.items() if score_name != deleted_scorer_name}


        write_eval_log(log, log.location)


# def run_analysis(df, input_params, output_colname, fnc):
#     """
#     Apply a function to specified columns of a dataframe.

#     Args:
#         df: Input dataframe
#         input_params: List of column names to pass to the function
#         output_colname: Name for the output column
#         fnc: Function to apply to the specified columns

#     Returns:
#         DataFrame with the results in output_colname, same index as original
#     """

#     # Apply function to specified columns
#     result = df[input_params].apply(lambda row: fnc(*row), axis=1)

#     # Create output dataframe with same index
#     output_df = pd.DataFrame({output_colname: result}, index=df.index)

#     return output_df