import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv_helper

# read the dataset into a data table using Pandas
df = csv_helper.get_dataframe()

# distribution of 'remaining_lease'
remainingLease_grpData = df.groupby('remaining_lease').size()
remainingLease_df = pd.Series(remainingLease_grpData)
print(remainingLease_df)

# Plot Histogram of Remaining Lease over the years
plt.bar(range(len(remainingLease_df)), remainingLease_df.values, align='center')
plt.xticks(range(len(remainingLease_df)), remainingLease_df.index.values, size='small')
plt.show()