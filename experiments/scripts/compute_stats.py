
import pandas as pd
import numpy as np
from scipy import stats


# Define a function to calculate the margin error
def calculate_margin_error(x, confidence_level=0.99):
    n = len(x)
    return stats.sem(x) * stats.t.ppf((1 + confidence_level) / 2, n - 1)


# Read the CSV file into a pandas DataFrame
data = pd.read_csv('../consolidated_data.csv')

# Group the data by the 'label' column
grouped_data = data.groupby('label')

# Calculate the average and confidence interval for each column within each label group
result = grouped_data.agg({'aoi': ['mean', calculate_margin_error],
                           'total_latency': ['mean', calculate_margin_error],
                           'number_of_requests_to_provider': ['mean', calculate_margin_error],
                           'hit_rate': ['mean', calculate_margin_error]})


# Flatten the column multi-index
result.columns = ['_'.join(col) for col in result.columns]


# Reset the index to make 'label' a regular column
result = result.reset_index()
print(result)
# Save the results to a new CSV file
result.to_csv('metrics_calculated.csv', index=False)


def calculate_confidence_interval(confidence_level, means):
    """
    Calculate the confidence interval for a given confidence level and an array of means.

    Parameters:
    -----------
    confidence_level : float
        The desired confidence level, ranging from 0 to 1.
    means : array-like
        An array of mean values.

    Returns:
    --------
    tuple
        A tuple containing the lower and upper bounds of the confidence interval.
    """
    means = np.array(means)
    n = len(means)
    mean = np.mean(means)
    std_err = np.std(means, ddof=1) / np.sqrt(n)
    margin_error = std_err * stats.t.ppf((1 + confidence_level) / 2, n - 1)
    return margin_error
