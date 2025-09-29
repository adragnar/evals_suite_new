import pandas as pd
import regex as re


def task_func(text):
    """
    Extract data from a text and create a Pandas DataFrame. The text contains several lines, each formatted as 'Score: 85, Category: Math'. Make sure to convert the scores in integer.

    Parameters:
    text (str): The text to analyze.

    Returns:
    DataFrame: A pandas DataFrame with extracted data.

    Requirements:
    - pandas
    - regex

    Example:
    >>> text = "Score: 85, Category: Math\\nScore: 90, Category: Science\\nScore: 80, Category: Math"
    >>> df = task_func(text)
    >>> print(df)
       Score Category
    0     85     Math
    1     90  Science
    2     80     Math
    """

    pattern = r"Score: (.*?), Category: (.*?)(\n|$)"
    matches = re.findall(pattern, text)
    data = [
        match[:2] for match in matches
    ]  # Extracting only the score and category from each match
    df = pd.DataFrame(data, columns=["Score", "Category"])
    df["Score"] = df["Score"].astype(int)
    return df
