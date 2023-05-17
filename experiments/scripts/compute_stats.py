import pandas as pd
import numpy as np
from scipy import stats

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('../consolidated_data.csv')

# Group the data by the 'label' column
grouped_data = data.groupby('label')

# Calculate the average and confidence interval for each column within each label group
result = grouped_data.agg({'aoi': ['mean', lambda x: stats.t.interval(0.99, len(x)-1, loc=np.mean(x), scale=stats.sem(x))],
                           'total_latency': ['mean', lambda x: stats.t.interval(0.99, len(x)-1, loc=np.mean(x), scale=stats.sem(x))],
                           'number_of_requests_to_provider': ['mean', lambda x: stats.t.interval(0.99, len(x)-1, loc=np.mean(x), scale=stats.sem(x))],
                           'hit_rate': ['mean', lambda x: stats.t.interval(0.99, len(x)-1, loc=np.mean(x), scale=stats.sem(x))]})

# Print the results
print(result)
result.to_csv('output_file.csv', index=False)
import pandas as pd
import numpy as np
from scipy import stats

# Read the CSV file into a pandas DataFrame
data = pd.read_csv('../consolidated_data.csv')

# Group the data by the 'label' column
grouped_data = data.groupby('label')

# Calculate the average and confidence interval for each column within each label group
result = grouped_data.agg({'aoi': ['mean', lambda x: stats.t.interval(0.99, len(x)-1, loc=np.mean(x), scale=stats.sem(x))],
                           'total_latency': ['mean', lambda x: stats.t.interval(0.99, len(x)-1, loc=np.mean(x), scale=stats.sem(x))],
                           'number_of_requests_to_provider': ['mean', lambda x: stats.t.interval(0.99, len(x)-1, loc=np.mean(x), scale=stats.sem(x))],
                           'hit_rate': ['mean', lambda x: stats.t.interval(0.99, len(x)-1, loc=np.mean(x), scale=stats.sem(x))]})

# Flatten the column multi-index
result.columns = ['_'.join(col) for col in result.columns]

# Reset the index to make 'label' a regular column
result = result.reset_index()

# Save the results to a new CSV file
result.to_csv('output_file.csv', index=False)
