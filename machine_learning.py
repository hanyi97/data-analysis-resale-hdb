import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from sklearn.metrics import mean_absolute_error
import data_helper
from tabulate import tabulate

# read the dataset into a data table using Pandas
df = data_helper.get_dataframe()

# delete the possible features that are not correlated to the resale price, in the dataframe
del df['year']
del df['month']
del df['block']
del df['street_name']
del df['storey_range']
del df['region']
del df['remaining_lease']
del df['lease_commence_date']

# Replace categorical data with one-hot encoded data
features_df = pd.get_dummies(df, columns=['flat_model', 'flat_type', 'town'])

# Remove the sale price from the feature data
del features_df['resale_price']

# Create the X and y arrays
X = features_df.values
y = df['resale_price'].values

# Split the data set in a training set (70%) and a test set (30%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=7)

# Fit regression model
model = ensemble.GradientBoostingRegressor(
    n_estimators=2000,  # how many decision trees to build
    learning_rate=0.1,  # how much decision trees influence overall prediction
    max_depth=6,
    min_samples_leaf=9,
    max_features=0.1,
    loss='huber',
    random_state=7
)
model.fit(X_train, y_train)

# Find the error rate on the training set
mse_train = mean_absolute_error(y_train, model.predict(X_train))

# Find the error rate on the test set
mse_test = mean_absolute_error(y_test, model.predict(X_test))

# description of resale price in table format
mse_table = [['Training Set Mean Absolute Error:', mse_train],
             ['Test Set Mean Absolute Error:', mse_test]]

print(tabulate(mse_table, tablefmt='simple', numalign='right', floatfmt='.4f'))
